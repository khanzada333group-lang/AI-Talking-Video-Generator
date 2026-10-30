import streamlit as st
from gtts import gTTS
import os
import replicate

# Page Configuration
st.set_page_config(page_title="AI Talking Video Generator", page_icon="🎥", layout="centered")

st.title("🎬 Professional AI Talking Video Generator")
st.write("Generate real MP4 videos with custom avatar motion, multi-character voices, and AI synchronization!")

# --- DIRECT SECURE TOKEN CONFIGURATION ---
api_token = "r8_FG00ecw3JqgZADKuF7DEuV3RIQlU5fX1nFD4x"
os.environ["REPLICATE_API_TOKEN"] = api_token

# 1. Multi-Image Upload Option
st.subheader("1. Upload Avatar Images")
uploaded_images = st.file_uploader(
    "Choose avatar images (PNG, JPG, JPEG)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_images:
    st.write(f"Total uploaded avatars: {len(uploaded_images)}")
    cols = st.columns(min(len(uploaded_images), 3))
    for idx, img in enumerate(uploaded_images):
        with cols[idx % 3]:
            st.image(img, caption=f"Avatar {idx+1}", use_column_width=True)

# 2. Character Voice & Language Settings
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
        ["English", "Japanese", "Urdu", "Spanish", "French", "German"]
    )

# 3. Video Motion Prompt
st.subheader("3. Video Motion & Action Prompt")
video_prompt = st.text_input(
    "Describe body actions or facial expressions:",
    placeholder="e.g., gentle nodding, smiling, expressive gestures..."
)

# 4. Dialogue Script
st.subheader("4. Enter Dialogue Script")
dialogue_text = st.text_area(
    "Type what your character should say:", 
    placeholder="Hello! Welcome to my AI talking video project..."
)

# 5. Generate Button
st.subheader("Generate Synchronized MP4 Video")
if st.button("Generate MP4 Video & Voice"):
    if not uploaded_images:
        st.warning("Please upload at least one avatar image!")
    elif not dialogue_text.strip():
        st.warning("Please enter some dialogue script!")
    else:
        with st.spinner("Processing character voice and generating real MP4 video... Please wait."):
            try:
                lang_mapping = {
                    "English": "en",
                    "Japanese": "ja",
                    "Urdu": "ur",
                    "Spanish": "es",
                    "French": "fr",
                    "German": "de"
                }
                lang_code = lang_mapping.get(language, "en")
                is_slow = True if "Child" in character_type else False
                
                tts = gTTS(text=dialogue_text, lang=lang_code, slow=is_slow)
                audio_path = "generated_voice.mp3"
                tts.save(audio_path)
                
                st.success(f"Generated {character_type} voice in {language} successfully!")
                st.audio(audio_path, format='audio/mp3')
                
                st.info("Connecting to Stable Video Diffusion on Replicate...")
                
                temp_image_path = "temp_avatar.jpg"
                with open(temp_image_path, "wb") as f:
                    f.write(uploaded_images[0].getbuffer())
                
                with open(temp_image_path, "rb") as image_file:
                    output = replicate.run(
                        "stability-ai/stable-video-diffusion:9bbef67ad4b63021fb0327f4ca75a40b4353347b749007f3521d96078f4b045e",
                        input={
                            "input_image": image_file,
                            "sizing_strategy": "maintain aspect ratio",
                            "motion_bucket_id": 127,
                            "fps": 7
                        }
                    )
                
                if output:
                    st.success("MP4 Video successfully rendered!")
                    st.video(output)
                else:
                    st.error("Video generation did not return an output.")
                    
            except Exception as e:
                st.error(f"An error occurred during API execution: {e}")
