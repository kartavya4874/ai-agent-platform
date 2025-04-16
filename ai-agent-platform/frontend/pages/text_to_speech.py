import streamlit as st
import requests
import os
import base64

# API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

def app():
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
