import streamlit as st
import requests
import json
import os
import base64
from PIL import Image
from io import BytesIO

# API endpoint - use environment variable in production
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

# Configure page
st.set_page_config(
    page_title="AI Agent Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .tool-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border: a 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    .success-msg {
        padding: 1rem;
        background-color: #d4edda;
        color: #155724;
        border-radius: 0.25rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "current_tool" not in st.session_state:
    st.session_state.current_tool = "Home"

# Helper functions
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

def switch_tool(tool_name):
    """Switch to a different tool"""
    st.session_state.current_tool = tool_name
    st.rerun()

# Sidebar
st.sidebar.markdown("<h1 style='text-align: center;'>🤖 AI Agent Platform</h1>", unsafe_allow_html=True)
st.sidebar.divider()

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
                if username and password:
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
                            st.rerun()
                        else:
                            st.error("Login failed. Please check your credentials.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                else:
                    st.warning("Please fill in all fields")
    
    elif auth_option == "Register":
        with st.sidebar.form("register_form"):
            st.subheader("Register")
            email = st.text_input("Email")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if email and username and password:
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
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {response.json()['detail']}")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                else:
                    st.warning("Please fill in all fields")
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.token = None
        st.session_state.user_id = None
        st.rerun()
    
    # Tool selection
    st.sidebar.divider()
    st.sidebar.header("Tools")
    
    for tool in ["Home", "Image Generator", "Code Assistant", "Writing Tool", "Text-to-Speech", "PowerPoint Generator"]:
       if st.sidebar.button(tool, key=f"sidebar_{tool}"):
            switch_tool(tool)
    
    # Subscription info
    st.sidebar.divider()
    st.sidebar.subheader("Subscription")
    
    subscription_status = "Free Trial"
    st.sidebar.info(f"Current Plan: {subscription_status}")
    
    if st.sidebar.button("Upgrade to Premium", type="primary"):
        # In a complete implementation, this would redirect to a checkout page
        st.sidebar.warning("Premium subscription coming soon!")

# Main content area
if not st.session_state.authenticated:
    st.markdown("<h1 class='main-header'>Welcome to AI Agent Platform</h1>", unsafe_allow_html=True)
    st.write("Please login or register to access our powerful AI tools.")
    
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.markdown("### 📷 Image Generator")
        st.write("Create custom images from text descriptions")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.markdown("### 💻 Code Assistant")
        st.write("Get help with coding and programming tasks")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.markdown("### ✍️ Writing Tool")
        st.write("Generate and improve written content")
        st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.markdown("### 🔊 Text-to-Speech")
        st.write("Convert text to natural-sounding speech")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 PowerPoint Generator")
        st.write("Create presentation slides automatically")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # Display selected tool based on session state
    current_tool = st.session_state.current_tool
    
    if current_tool == "Home":
        st.markdown("<h1 class='main-header'>AI Agent Platform</h1>", unsafe_allow_html=True)
        st.write(f"Welcome back, {st.session_state.username}! Select a tool to get started.")
        
        st.subheader("Your AI Toolkit")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
            st.markdown("### 📷 Image Generator")
            st.write("Create custom images from text descriptions")
            if st.button("Open Image Generator", key="home_img"):
                switch_tool("Image Generator")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
            st.markdown("### 💻 Code Assistant")
            st.write("Get help with coding and programming tasks")
            if st.button("Open Code Assistant", key="home_code"):
                switch_tool("Code Assistant")
            st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
            st.markdown("### ✍️ Writing Tool")
            st.write("Generate and improve written content")
            if st.button("Open Writing Tool", key="home_write"):
                switch_tool("Writing Tool")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
            st.markdown("### 🔊 Text-to-Speech")
            st.write("Convert text to natural-sounding speech")
            if st.button("Open Text-to-Speech", key="home_tts"):
                switch_tool("Text-to-Speech")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 PowerPoint Generator")
        st.write("Create presentation slides automatically")
        if st.button("Open PowerPoint Generator", key="home_ppt"):
            switch_tool("PowerPoint Generator")
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif current_tool == "Image Generator":
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
    
    elif current_tool == "Code Assistant":
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
    
    elif current_tool == "Writing Tool":
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
    
    elif current_tool == "Text-to-Speech":
        st.markdown("<h1 class='main-header'>AI Text-to-Speech</h1>", unsafe_allow_html=True)
        st.write("Convert text to natural-sounding speech using AI.")
        
        with st.form("tts_form"):
            text = st.text_area("Enter text to convert to speech:", height=150,
                            placeholder="Enter the text you want to convert to speech...")
            
            col1, col2 = st.columns(2)
            with col1:
                voice = st.selectbox("Voice:", ["Male (en-US-Neural2-D)", "Female (en-US-Neural2-F)", "Neutral (en-US-Neural2-A)"])
            
            with col2:
                language = st.selectbox("Language:", ["English", "Spanish", "French", "German", "Japanese"])
            
            submit = st.form_submit_button("Generate Speech")
        
        if submit and text:
            with st.spinner("Converting text to speech..."):
                voice_id = voice.split(" ")[1].strip("()")
                
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
                    response = requests.post(
                        f"{API_URL}/tools/text-to-speech",
                        params={"text": text, "voice": voice_id},
                        headers=headers
                    )
                                           
                    if response.status_code == 200:
                        result = response.json()
                        if result["success"]:
                            st.success("Text converted to speech!")
                            
                            # Show audio player if file exists
                            file_path = result["file_path"]
                            if "message" in result:
                                st.info(result["message"])
                                st.write("In a complete implementation, this would include audio playback.")
                            else:
                                try:
                                    with open(file_path, "rb") as f:
                                        audio_bytes = f.read()
                                    st.audio(audio_bytes, format="audio/mp3")
                                except Exception as e:
                                    st.warning(f"Could not play audio: {str(e)}")
                            
                            # Add download button
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
    
    elif current_tool == "PowerPoint Generator":
        st.markdown("<h1 class='main-header'>AI PowerPoint Generator</h1>", unsafe_allow_html=True)
        st.write("Create presentation slides automatically using AI.")
        
        with st.form("ppt_form"):
            topic = st.text_input("Presentation Topic:", placeholder="E.g., Artificial Intelligence Trends 2025")
            
            col1, col2 = st.columns(2)
            with col1:
                num_slides = st.slider("Number of Slides:", min_value=3, max_value=15, value=5)
            
            with col2:
                template = st.selectbox("Presentation Template:", 
                                    ["Professional (Blue)", "Creative (Purple)", "Minimal (White)", "Default"])
            
            # Map frontend template names to backend values
            template_map = {
                "Professional (Blue)": "professional",
                "Creative (Purple)": "creative",
                "Minimal (White)": "minimal",
                "Default": "default"
            }
            
            instructions = st.text_area("Additional Instructions:", height=100,
                                    placeholder="E.g., Include data visualizations and focus on practical applications")
            
            submit = st.form_submit_button("Generate Presentation")
            
            if submit and topic:
                with st.spinner("Generating your presentation..."):
                    full_prompt = f"Create a {num_slides}-slide presentation about {topic}. {instructions}"
                    
                    try:
                        headers = {"Authorization": f"Bearer {st.session_state.token}"} if "token" in st.session_state else {}
                        response = requests.post(
                            f"{API_URL}/tools/generate-presentation",
                            params={
                                "prompt": full_prompt, 
                                "slides": num_slides,
                                "template": template_map[template]
                            },
                            headers=headers
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            if result["success"]:
                                st.success("Presentation generated successfully!")
                                
                                # Add download button
                                file_path = result["file_path"]
                                file_name = f"{topic.replace(' ', '_')}.pptx"
                                download_button(file_path, "Download Presentation", file_name)
                                
                                # Show preview image based on template
                                if template == "Professional (Blue)":
                                    st.image("https://via.placeholder.com/640x360/00416C/FFFFFF?text=Professional+Template+Preview", 
                                            caption="Professional Template Preview")
                                elif template == "Creative (Purple)":
                                    st.image("https://via.placeholder.com/640x360/6E2B62/FFFFFF?text=Creative+Template+Preview", 
                                            caption="Creative Template Preview")
                                elif template == "Minimal (White)":
                                    st.image("https://via.placeholder.com/640x360/FFFFFF/505050?text=Minimal+Template+Preview", 
                                            caption="Minimal Template Preview")
                                else:
                                    st.image("https://via.placeholder.com/640x360/E0E0E0/303030?text=Default+Template+Preview", 
                                            caption="Default Template Preview")
                            else:
                                st.error("Failed to generate presentation")
                        else:
                            st.error(f"API Error: {response.status_code}")
                    
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            elif submit:
                st.warning("Please enter a topic for your presentation")

# Footer
st.divider()
st.markdown("<div style='text-align: center; color: gray;'>© 2025 AI Agent Platform | Developed by Kartavya Baluja</div>", unsafe_allow_html=True)
