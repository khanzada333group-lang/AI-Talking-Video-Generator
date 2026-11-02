import streamlit as st
from gtts import gTTS
import os
import requests

# Page Configuration
st.set_page_config(
    page_title="Professional AI Talking Video Generator", 
    page_icon="🎬", 
    layout="centered"
)

st.title("🎬 Professional AI Talking Video Generator")
st.write("Generate real MP4 videos and multi-language voiceovers instantly and seamlessly!")

# --- SECURE FIXED HUGGING FACE TOKEN ---
# (Yahan aap apna Hugging Face token aik baar likh dein gay, yوزر ko kabhi nazar nahi aey ga)
HF_TOKEN = "yahan_apna_huggingface_token_likh_lein"  # e.g., "hf_xxxxxxxxxxxxxxxx"

# 1. Image Upload
st.subheader("1. Upload Avatar Image")
uploaded_image = st.file_uploader(
    "Choose an avatar image (PNG, JPG, JPEG)", 
    type=["png", "jpg", "jpeg"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Selected Avatar", width=250)

# 2. Voice Settings
st.subheader("2. Character Voice & Language Settings")
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

# 3. Dialogue Script
st.subheader("3. Enter Dialogue Script")
dialogue_text = st.text_area(
    "Type what your character should say:", 
    placeholder="Hello! Welcome to my AI talking video project..."
)

# 4. Generate Button
st.subheader("Generate Professional MP4 Video")
if st.button("✨ Generate Video & Voice", type="primary"):
    if not uploaded_image:
        st.warning("⚠️ Please upload an avatar image!")
    elif not dialogue_text.strip():
        st.warning("⚠️ Please enter some dialogue script!")
    else:
        with st.spinner("Processing voice and rendering real MP4 video... Please wait a moment."):
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
                
                st.info("Rendering real MP4 video via AI...")
                
                # 2. Call Hugging Face API Automatically
                API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"
                headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                
                image_bytes = uploaded_image.getvalue()
                response = requests.post(API_URL, headers=headers, data=image_bytes)
                
                if response.status_code == 200:
                    video_path = "generated_video.mp4"
                    with open(video_path, "wb") as f:
                        f.write(response.content)
                    
                    st.success("🎉 MP4 Video Successfully Generated!")
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
                    st.error(f"API Error ({response.status_code}): Please make sure you added your valid Hugging Face token in the code!")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
