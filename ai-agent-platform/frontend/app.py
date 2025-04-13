import streamlit as st
import requests
import json
import os
import base64
from PIL import Image
from io import BytesIO

# API endpoint
API_URL = "http://localhost:8000/api"

# Configure page
st.set_page_config(
    page_title="AI Agent Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Helper functions
def download_button(file_path, button_text, file_name):
    with open(file_path, "rb") as file:
        contents = file.read()
    
    b64 = base64.b64encode(contents).decode()
    href = f'data:application/octet-stream;base64,{b64}'
    return st.markdown(f'<a href="{href}" download="{file_name}">{button_text}</a>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("AI Agent Platform")

# Authentication section
if not st.session_state.authenticated:
    auth_option = st.sidebar.radio("Authentication", ["Login", "Register"])
    
    if auth_option == "Login":
        with st.sidebar.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                try:
                    response = requests.post(
                        f"{API_URL}/auth/token",
                        data={"username": username, "password": password}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data["access_token"]
                        st.session_state.username = username
                        st.session_state.authenticated = True
                        st.experimental_rerun()
                    else:
                        st.error("Login failed. Please check your credentials.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    elif auth_option == "Register":
        with st.sidebar.form("register_form"):
            st.subheader("Register")
            email = st.text_input("Email")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                try:
                    response = requests.post(
                        f"{API_URL}/auth/register",
                        json={"email": email, "username": username, "password": password}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data["access_token"]
                        st.session_state.username = username
                        st.session_state.authenticated = True
                        st.success("Registration successful!")
                        st.experimental_rerun()
                    else:
                        st.error(f"Registration failed: {response.json()['detail']}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.token = None
        st.session_state.user_id = None
        st.experimental_rerun()
    
    # Tool selection
    tool = st.sidebar.selectbox(
        "Select Tool",
        ["Home", "Image Generator", "Code Assistant", "Writing Tool", "Text-to-Speech", "PowerPoint Generator"]
    )
    
    # Subscription info
    st.sidebar.subheader("Subscription")
    st.sidebar.info("Free Trial")
    if st.sidebar.button("Upgrade"):
        st.sidebar.markdown("[Upgrade to Premium](http://localhost:8000/api/subscription/upgrade)")

# Main content area
if not st.session_state.authenticated:
    st.title("Welcome to AI Agent Platform")
    st.write("Please login or register to access the AI tools.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📷 **Image Generator**")
        st.write("Create custom images from text descriptions")
    
    with col2:
        st.info("💻 **Code Assistant**")
        st.write("Get help with coding and programming tasks")
    
    with col3:
        st.info("✍️ **Writing Tool**")
        st.write("Generate and improve written content")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🔊 **Text-to-Speech**")
        st.write("Convert text to natural-sounding speech")
    
    with col2:
        st.info("📊 **PowerPoint Generator**")
        st.write("Create presentation slides automatically")
else:
    # Display selected tool
    if tool == "Home":
        st.title("AI Agent Platform")
        st.write(f"Welcome back, {st.session_state.username}!")
        
        st.header("Your AI Toolkit")
        st.write("Select a tool from the sidebar to get started.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("📷 **Image Generator**")
            st.write("Create custom images from text descriptions")
            if st.button("Go to Image Generator", key="home_img"):
                tool = "Image Generator"
                st.experimental_rerun()
        
        with col2:
            st.info("💻 **Code Assistant**")
            st.write("Get help with coding and programming tasks")
            if st.button("Go to Code Assistant", key="home_code"):
                tool = "Code Assistant"
                st.experimental_rerun()
        
        with col3:
            st.info("✍️ **Writing Tool**")
            st.write("Generate and improve written content")
            if st.button("Go to Writing Tool", key="home_write"):
                tool = "Writing Tool"
                st.experimental_rerun()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("🔊 **Text-to-Speech**")
            st.write("Convert text to natural-sounding speech")
            if st.button("Go to Text-to-Speech", key="home_tts"):
                tool = "Text-to-Speech"
                st.experimental_rerun()
        
        with col2:
            st.info("📊 **PowerPoint Generator**")
            st.write("Create presentation slides automatically")
            if st.button("Go to PowerPoint Generator", key="home_ppt"):
                tool = "PowerPoint Generator"
                st.experimental_rerun()
    
    elif tool == "Image Generator":
        st.title("AI Image Generator")
        
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
                    response = requests.post(
                        f"{API_URL}/tools/generate-image",
                        params={"prompt": prompt, "style": style}
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
    
    elif tool == "Code Assistant":
        st.title("AI Code Assistant")
        
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
                    response = requests.post(
                        f"{API_URL}/tools/generate-code",
                        params={"prompt": prompt, "language": language}
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
    
    elif tool == "Writing Tool":
        st.title("AI Writing Tool")
        
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
                    response = requests.post(
                        f"{API_URL}/tools/generate-document",
                        params={"prompt": full_prompt, "format": format_type.lower()}
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
    
    elif tool == "Text-to-Speech":
        st.title("AI Text-to-Speech")
        
        with st.form("tts_form"):
            text = st.text_area("Enter text to convert to speech:", height=150,
                            placeholder="Enter the text you want to convert to speech...")
            
            col1, col2 = st.columns(2)
            with col1:
                voice = st.selectbox("Voice:", ["Male", "Female", "Neutral"])
            
            with col2:
                language = st.selectbox("Language:", ["English", "Spanish", "French", "German", "Japanese"])
            
            submit = st.form_submit_button("Generate Speech")
        
        if submit and text:
            with st.spinner("Converting text to speech..."):
                try:
                    response = requests.post(
                        f"{API_URL}/tools/text-to-speech",
                        params={"text": text}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result["success"]:
                            st.success("Text converted to speech!")
                            st.info(result["message"])
                            
                            # In a real implementation, you would play the audio
                            st.write("In a complete implementation, this would include audio playback.")
                            
                            # Add download button
                            file_path = result["file_path"]
                            file_name = "generated_speech.mp3"
                            download_button(file_path, "Download Audio", file_name)
                        else:
                            st.error("Failed to convert text to speech")
                    else:
                        st.error(f"API Error: {response.status_code}")
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        elif submit:
            st.warning("Please enter text to convert to speech")
    
    elif tool == "PowerPoint Generator":
        st.title("AI PowerPoint Generator")
        
        with st.form("ppt_form"):
            topic = st.text_input("Presentation Topic:", placeholder="E.g., Artificial Intelligence Trends 2025")
            
            num_slides = st.slider("Number of Slides:", min_value=3, max_value=15, value=5)
            
            instructions = st.text_area("Additional Instructions:", height=100,
                                    placeholder="E.g., Include data visualizations and focus on practical applications")
            
            submit = st.form_submit_button("Generate Presentation")
        
        if submit and topic:
            with st.spinner("Generating your presentation..."):
                full_prompt = f"Create a {num_slides}-slide presentation about {topic}. {instructions}"
                
                try:
                    response = requests.post(
                        f"{API_URL}/tools/generate-presentation",
                        params={"prompt": full_prompt, "slides": num_slides}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result["success"]:
                            st.success("Presentation generated successfully!")
                            
                            # Add download button
                            file_path = result["file_path"]
                            file_name = f"{topic.replace(' ', '_')}.pptx"
                            download_button(file_path, "Download Presentation", file_name)
                        else:
                            st.error("Failed to generate presentation")
                    else:
                        st.error(f"API Error: {response.status_code}")
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        elif submit:
            st.warning("Please enter a topic for your presentation")
