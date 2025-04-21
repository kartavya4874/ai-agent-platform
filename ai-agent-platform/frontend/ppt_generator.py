import streamlit as st
import requests
import os
import base64

# API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

def app():
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
