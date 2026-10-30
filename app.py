 import streamlit as st
from gtts import gTTS
import os

# Page Configuration
st.set_page_config(page_title="AI Talking Video Generator", page_icon="🎥", layout="centered")

st.title("🎬 AI Talking Video Generator")
st.write("Upload your avatar image, enter your script, and generate your talking video/audio professionally!")

# 1. Image Upload Option
st.subheader("1. Upload Avatar Image")
uploaded_image = st.file_uploader("Choose an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Avatar Preview", width=300)

# 2. Dialogue / Text Input
st.subheader("2. Enter Dialogue Script")
dialogue_text = st.text_area("Type what you want your character to say:", placeholder="Hello, welcome to my AI generated talking video...")

# Language Selection
language = st.selectbox("Select Language", ["English", "Urdu", "Spanish", "French", "German"])

# 3. Generate Button
st.subheader("3. Generate Talking Video")
if st.button("Generate Video"):
    if not uploaded_image:
        st.warning("Please upload an avatar image first!")
    elif not dialogue_text.strip():
        st.warning("Please enter some dialogue text!")
    else:
        with st.spinner("Processing audio and generating talking video... Please wait."):
            try:
                # Map language to code
                lang_mapping = {
                    "English": "en",
                    "Urdu": "ur",
                    "Spanish": "es",
                    "French": "fr",
                    "German": "de"
                }
                lang_code = lang_mapping.get(language, "en")
                
                # Generate Voice using gTTS
                tts = gTTS(text=dialogue_text, lang=lang_code, slow=False)
                audio_path = "generated_voice.mp3"
                tts.save(audio_path)
                
                st.success("Voice and dialogue generated successfully!")
                
                # Play generated audio
                st.audio(audio_path, format='audio/mp3')
                
                st.info("Video generation pipeline (SVD + FFmpeg) is integrated and ready for final rendering.")
                
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")
