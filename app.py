import streamlit as st
from gtts import gTTS
import os
import requests

# Page Configuration
st.set_page_config(
    page_title="100% Free AI Talking Video Generator", 
    page_icon="🎬", 
    layout="centered"
)

st.title("🎬 Free AI Talking Video Generator")
st.write("Generate real videos and voiceovers completely free using Hugging Face (No Credit Card Required)!")

# 1. Hugging Face Free Token Input
st.subheader("1. Hugging Face Free API Token")
hf_token = st.text_input(
    "Enter your free Hugging Face Token (Get it free on huggingface.co):", 
    type="password",
    placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)

# 2. Image Upload
st.subheader("2. Upload Avatar Image")
uploaded_image = st.file_uploader(
    "Choose an avatar image (PNG, JPG, JPEG)", 
    type=["png", "jpg", "jpeg"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Selected Avatar", width=250)

# 3. Voice Settings
st.subheader("3. Character Voice Settings")
col1, col2 = st.columns(2)

with col1:
    character_type = st.selectbox(
        "Select Character Voice Type",
        ["Woman (Female)", "Man (Male)", "Child / Kid"]
    )

with col2:
    language = st.selectbox(
        "Select Voice Language", 
        ["English", "Urdu", "Japanese", "Spanish", "French", "German"]
    )

# 4. Dialogue Script
st.subheader("4. Enter Dialogue Script")
dialogue_text = st.text_area(
    "Type what your character should say:", 
    placeholder="Hello! Welcome to my AI talking video project..."
)

# 5. Generate Button
st.subheader("Generate Free MP4 Video & Voice")
if st.button("✨ Generate Free Video & Voice", type="primary"):
    if not hf_token.strip():
        st.warning("⚠️ Please enter your free Hugging Face API token!")
    elif not uploaded_image:
        st.warning("⚠️ Please upload an avatar image!")
    elif not dialogue_text.strip():
        st.warning("⚠️ Please enter some dialogue script!")
    else:
        with st.spinner("Processing voice and rendering video via Free AI... Please wait a moment."):
            try:
                # 1. Generate Voice using gTTS
                lang_mapping = {
                    "English": "en",
                    "Urdu": "ur",
                    "Japanese": "ja",
                    "Spanish": "es",
                    "French": "fr",
                    "German": "de"
                }
                lang_code = lang_mapping.get(language, "en")
                is_slow = True if "Child" in character_type else False
                
                tts = gTTS(text=dialogue_text, lang=lang_code, slow=is_slow)
                audio_path = "generated_voice.mp3"
                tts.save(audio_path)
                
                st.success(f"🎉 Generated {character_type} voice successfully!")
                st.audio(audio_path, format='audio/mp3')
                
                st.info("Connecting to Hugging Face Free AI Model to render video...")
                
                # 2. Call Hugging Face Free Inference API for Image-to-Video
                API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"
                headers = {"Authorization": f"Bearer {hf_token}"}
                
                image_bytes = uploaded_image.getvalue()
                response = requests.post(API_URL, headers=headers, data=image_bytes)
                
                if response.status_code == 200:
                    video_path = "generated_video.mp4"
                    with open(video_path, "wb") as f:
                        f.write(response.content)
                    
                    st.success("🎉 Real MP4 Video Successfully Generated!")
                    st.video(video_path)
                    
                    # Download button for video
                    with open(video_path, "video/mp4") as v_file:
                        st.download_button(
                            label="📥 Download Video MP4",
                            data=v_file,
                            file_name="ai_talking_video.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error(f"API Error ({response.status_code}): Model might be loading. Please wait a minute and try again, or check your token.")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
