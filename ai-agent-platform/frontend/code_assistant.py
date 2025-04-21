import streamlit as st
import requests
import os
import base64

# API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

def app():
    st.markdown("<h1 class='main-header'>AI Code Assistant</h1>", unsafe_allow_html=True)
    st.write("Get help with coding tasks using AI.")
    
    with st.form("code_assistant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.selectbox("Programming Language", 
                                ["Python", "JavaScript", "Java", "C++", "Go", "SQL", "HTML/CSS", "Other"])
        
        with col2:
            task = st.selectbox("Task Type", 
                            ["Write Code", "Debug Code", "Explain Code", "Optimize Code"])
        
        prompt = st.text_area("Describe what you need or paste your code:", height=200,
                          placeholder="E.g., Write a function to calculate Fibonacci numbers")
        
        submit = st.form_submit_button("Generate Code")
    
    if submit and prompt:
        with st.spinner("Generating your code..."):
            try:
                headers = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
                response = requests.post(
                    f"{API_URL}/tools/generate-code",
                    params={"prompt": f"{task}: {prompt}", "language": language.lower()},
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        st.success("Code generated successfully!")
                        
                        # Display the code
                        st.code(result["code"], language=language.lower())
                        
                        # Add download button
                        file_path = result["file_path"]
                        file_name = os.path.basename(file_path)
                        download_button(file_path, "Download Code", file_name)
                    else:
                        st.error("Failed to generate code")
                else:
                    st.error(f"API Error: {response.status_code}")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    elif submit:
        st.warning("Please describe what you need")

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
