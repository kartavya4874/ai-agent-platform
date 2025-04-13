import os
import httpx
import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User, UserContent
from app.services.openai_service import OpenAIService
from typing import Optional
from io import BytesIO
import pptx
from pptx.util import Inches, Pt
from docx import Document
import tempfile
import shutil
import requests
from PIL import Image

router = APIRouter()

# Helper function to get temporary file path
def get_temp_file_path(filename):
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, filename)

@router.post("/generate-image")
async def generate_image(prompt: str, style: Optional[str] = "realistic"):
    """Generate an image based on text prompt"""
    full_prompt = f"{prompt} in {style} style"
    
    # Call OpenAI to generate image
    image_url = await OpenAIService.generate_image(full_prompt)
    
    if not image_url:
        raise HTTPException(status_code=500, detail="Failed to generate image")
    
    # Download the image
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to download generated image")
        
        # Save to temporary file
        img_temp_path = get_temp_file_path(f"generated_image_{hash(prompt)}.png")
        with open(img_temp_path, "wb") as f:
            f.write(response.content)
    
    return {"image_path": img_temp_path, "success": True}

@router.post("/generate-code")
async def generate_code(prompt: str, language: str):
    """Generate code based on text prompt"""
    # Generate code
    code = await OpenAIService.generate_code(prompt, language)
    
    if not code:
        raise HTTPException(status_code=500, detail="Failed to generate code")
    
    # Determine file extension
    extensions = {
        "python": "py",
        "javascript": "js",
        "typescript": "ts",
        "java": "java",
        "c++": "cpp",
        "c#": "cs",
        "go": "go",
        "ruby": "rb",
        "php": "php",
        "swift": "swift",
        "kotlin": "kt",
        "rust": "rs",
        "sql": "sql",
        "html": "html",
        "css": "css"
    }
    
    ext = extensions.get(language.lower(), "txt")
    
    # Save to temporary file
    code_temp_path = get_temp_file_path(f"generated_code_{hash(prompt)}.{ext}")
    with open(code_temp_path, "w") as f:
        f.write(code)
    
    return {"code": code, "file_path": code_temp_path, "success": True}

@router.post("/generate-document")
async def generate_document(prompt: str, format: str = "docx"):
    """Generate a document based on text prompt"""
    # Generate content
    content = await OpenAIService.generate_text(prompt)
    
    if not content:
        raise HTTPException(status_code=500, detail="Failed to generate document content")
    
    if format.lower() == "docx":
        # Create a new Word document
        doc = Document()
        doc.add_heading('Generated Document', 0)
        
        # Add the content
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                if para.startswith('# '):
                    doc.add_heading(para[2:], level=1)
                elif para.startswith('## '):
                    doc.add_heading(para[3:], level=2)
                elif para.startswith('### '):
                    doc.add_heading(para[4:], level=3)
                else:
                    doc.add_paragraph(para)
        
        # Save the document
        doc_temp_path = get_temp_file_path(f"generated_document_{hash(prompt)}.docx")
        doc.save(doc_temp_path)
        
        return {"file_path": doc_temp_path, "success": True}
    
    elif format.lower() == "pdf":
        # For PDF, we'll create a simple text file for now
        # In a production app, you'd use a library like reportlab
        text_temp_path = get_temp_file_path(f"generated_document_{hash(prompt)}.txt")
        with open(text_temp_path, "w") as f:
            f.write(content)
        
        return {"file_path": text_temp_path, "success": True}
    
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

@router.post("/generate-presentation")
async def generate_presentation(prompt: str, slides: int = 5):
    """Generate a PowerPoint presentation based on text prompt"""
    # Generate content structure
    structure_prompt = f"Create a {slides}-slide presentation structure on the topic: {prompt}. For each slide, provide a title and bullet points. Format as 'Slide 1: Title\\n- Bullet 1\\n- Bullet 2'"
    
    structure = await OpenAIService.generate_text(structure_prompt)
    
    if not structure:
        raise HTTPException(status_code=500, detail="Failed to generate presentation structure")
    
    # Create PowerPoint presentation
    prs = pptx.Presentation()
    
    # Parse the structure and create slides
    current_slide = None
    slide_layout = prs.slide_layouts[1]  # Using title and content layout
    
    for line in structure.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('Slide ') and ':' in line:
            # New slide
            title = line.split(':', 1)[1].strip()
            current_slide = prs.slides.add_slide(slide_layout)
            current_slide.shapes.title.text = title
            current_content = current_slide.placeholders[1]
            content_text = current_content.text_frame
        
        elif line.startswith('- ') and current_slide:
            # Bullet point
            p = content_text.add_paragraph()
            p.text = line[2:].strip()
            p.level = 0
    
    # Save presentation
    ppt_temp_path = get_temp_file_path(f"generated_presentation_{hash(prompt)}.pptx")
    prs.save(ppt_temp_path)
    
    return {"file_path": ppt_temp_path, "success": True}

@router.post("/text-to-speech")
async def text_to_speech(text: str):
    """Convert text to speech"""
    # For now, we'll create a placeholder
    # In a complete implementation, you would use a TTS service like ElevenLabs, Google TTS, etc.
    
    # Create a placeholder text file for now
    tts_temp_path = get_temp_file_path(f"text_to_speech_{hash(text)}.txt")
    with open(tts_temp_path, "w") as f:
        f.write(f"Audio would be generated for: {text}")
    
    return {"file_path": tts_temp_path, "success": True, "message": "In a complete implementation, this would generate actual audio."}

@router.get("/download/{file_path:path}")
async def download_file(file_path: str):
    """Download generated files"""
    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get filename
    filename = os.path.basename(file_path)
    
    # Return file for download
    return FileResponse(path=file_path, filename=filename)
