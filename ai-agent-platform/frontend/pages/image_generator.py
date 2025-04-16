import streamlit as st
import requests
import os
import base64
from PIL import Image
from io import BytesIO

# API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

def app():
    st.markdown("<h1 class='main-header'>AI Image Generator</h1>", unsafe_allow_html=True)
    st.write("Create images from text descriptions using AI.")
    
    with st.form("image_generator_form"):
        prompt = st.text_area("Describe the image you want to generate:", height=100, 
                          placeholder="E.g., A serene mountain landscape with a lake at sunset")
        
        col1, col2 = st.columns(2)
        with col1:
            style = st.selectbox("Select style:", 
                             ["Realistic", "Digital Art", "Sketch", "Watercolor", "3D Render", "Anime"])
        
        with col2:
            size = st.selectbox("Image size:", ["512x512", "1024x1024"])
        
        submit = st.form_submit_button("Generate Image")
    
    if submit and prompt:
        with st.spinner("Generating your image..."):
            try:
                headers = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
                response = requests.post(
                    f"{API_URL}/tools/generate-image",
                    params={"prompt": prompt, "style": style.lower()},
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        st.success("Image generated successfully!")
                        # Display the image
                        image_path = result["image_path"]
                        st.image(image_path, caption="Generated Image")
                        
                        # Add download button
                        file_name = f"generated_image_{hash(prompt)}.png"
                        download_button(image_path, "Download Image", file_name)
                    else:
                        st.error("Failed to generate image")
                else:
                    st.error(f"API Error: {response.status_code}")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    elif submit:
        st.warning("Please enter a description for your image")

def download_button(file_path, button_text, file_name):
    """Create a download button for a file"""
    try:
        with open(file_path, "rb") as file:
            contents = file.read()
        
        b64 = base64.b64encode(contents).decode()
        href = f'data:application/octet-stream;base64,{b64}'
        return st.markdown(f'<a href="{href}" download="{file_name}" class="st-emotion-cache-1nf528h e1f1d6gn0">⬇️ {button_text}</a>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error creating download button: {str(e)}")
        return None
