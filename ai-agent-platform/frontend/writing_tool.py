import streamlit as st
import requests
import os
import base64

# API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

def app():
    st.markdown("<h1 class='main-header'>AI Writing Tool</h1>", unsafe_allow_html=True)
    st.write("Generate high-quality written content using AI.")
    
    with st.form("writing_tool_form"):
        document_type = st.selectbox("Document Type", 
                                 ["Essay", "Blog Post", "Report", "Email", "Creative Writing", "Summary"])
        
        topic = st.text_input("Topic or Title:", placeholder="E.g., The Impact of Artificial Intelligence on Healthcare")
        
        instructions = st.text_area("Additional Instructions:", height=100, 
                                placeholder="E.g., Include statistics and focus on recent advancements")
        
        format_type = st.selectbox("Output Format:", ["DOCX", "PDF", "Text"])
        
        submit = st.form_submit_button("Generate Document")
    
    if submit and topic:
        with st.spinner("Generating your document..."):
            full_prompt = f"Write a {document_type} about {topic}. {instructions}"
            
            try:
                headers = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
                response = requests.post(
                    f"{API_URL}/tools/generate-document",
                    params={"prompt": full_prompt, "format": format_type.lower()},
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        st.success("Document generated successfully!")
                        
                        # Add download button
                        file_path = result["file_path"]
                        file_name = f"{topic.replace(' ', '_')}.{format_type.lower()}"
                        download_button(file_path, "Download Document", file_name)
                    else:
                        st.error("Failed to generate document")
                else:
                    st.error(f"API Error: {response.status_code}")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    elif submit:
        st.warning("Please enter a topic for your document")

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
