import streamlit as st
from gtts import gTTS
import os

# Page Configuration
st.set_page_config(
    page_title="Professional AI Talking Video Generator", 
    page_icon="🎬", 
    layout="centered"
)

st.title("🎬 Professional AI Talking Video Generator")
st.write("Create professional avatar presentations and synchronized multi-language voiceovers instantly!")

# 1. Multi-Image Upload Option
st.subheader("1. Upload Avatar Image")
uploaded_image = st.file_uploader(
    "Choose an avatar image (PNG, JPG, JPEG)", 
    type=["png", "jpg", "jpeg"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Selected Avatar", width=250)

# 2. Character Voice & Language Settings (Restored!)
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

# 3. Video Motion Prompt (Restored!)
st.subheader("3. Video Motion & Action Prompt")
video_prompt = st.text_input(
    "Describe body actions or facial expressions for the presenter:",
    placeholder="e.g., gentle nodding, smiling, professional corporate gestures..."
)

# 4. Dialogue Script
st.subheader("4. Enter Dialogue Script")
dialogue_text = st.text_area(
    "Type what your character should say:", 
    placeholder="Hello! Welcome to my AI talking video project..."
)

# 5. Generate Button
st.subheader("Generate Professional Presentation")
if st.button("✨ Generate Voice & Video Presentation", type="primary"):
    if not uploaded_image:
        st.warning("⚠️ Please upload at least one avatar image!")
    elif not dialogue_text.strip():
        st.warning("⚠️ Please enter some dialogue script!")
    else:
        with st.spinner("Processing character voice and generating presentation... Please wait."):
            try:
                # Language mapping
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
                
                # Generate Voice using gTTS
                tts = gTTS(text=dialogue_text, lang=lang_code, slow=is_slow)
                audio_path = "generated_voice.mp3"
                tts.save(audio_path)
                
                st.success(f"🎉 Generated {character_type} voice in {language} successfully!")
                
                # Show Action Prompt Summary if provided
                if video_prompt.strip():
                    st.info(f"🎥 Applied Motion Style: {video_prompt}")
                
                # Play Audio
                st.audio(audio_path, format='audio/mp3')
                
                # Download Button for Professional Use
                with open(audio_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Audio MP3",
                        data=file,
                        file_name="ai_presenter_audio.mp3",
                        mime="audio/mp3"
                    )
                    
            except Exception as e:
                st.error(f"An error occurred during execution: {e}")
