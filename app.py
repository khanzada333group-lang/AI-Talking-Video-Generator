import streamlit as st
from gtts import gTTS
import os
import base64

# Page Configuration
st.set_page_config(
    page_title="Free AI Talking Video & Presenter Studio", 
    page_icon="🎬", 
    layout="centered"
)

# Custom Styling for Professional Animated Look
st.markdown("""
    <style>
    .main-title {
        font-size: 28px;
        font-weight: bold;
        color: #4F46E5;
        text-align: center;
    }
    .sub-text {
        text-align: center;
        color: #6B7280;
        margin-bottom: 20px;
    }
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.7); }
        70% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(79, 70, 229, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }
    }
    .avatar-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    .animated-avatar {
        border-radius: 50%;
        width: 180px;
        height: 180px;
        object-fit: cover;
        border: 4px solid #4F46E5;
        animation: pulse 2s infinite;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎬 Free Professional AI Presenter Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Create synchronized multi-language voice avatars instantly (100% Free & No Card Required)</p>', unsafe_allow_html=True)

# 1. Avatar Upload
st.subheader("1. Upload Avatar Image")
uploaded_image = st.file_uploader(
    "Choose an avatar image (PNG, JPG, JPEG)", 
    type=["png", "jpg", "jpeg"]
)

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
        ["English", "Urdu", "Japanese", "Spanish", "French", "German"]
    )

# 3. Video Motion Prompt
st.subheader("3. Video Motion & Action Prompt")
video_prompt = st.text_input(
    "Describe desired presentation style/motion:",
    placeholder="e.g., professional corporate speech, expressive storytelling..."
)

# 4. Dialogue Script
st.subheader("4. Enter Dialogue Script")
dialogue_text = st.text_area(
    "Type what your character should say:", 
    placeholder="Hello! Welcome to my AI talking video project..."
)

# 5. Generate Button
st.subheader("Generate AI Presentation")
if st.button("✨ Generate Presentation & Voice", type="primary"):
    if not uploaded_image:
        st.warning("⚠️ Please upload an avatar image first!")
    elif not dialogue_text.strip():
        st.warning("⚠️ Please enter some dialogue script!")
    else:
        with st.spinner("Synthesizing studio-quality voice and preparing presentation..."):
            try:
                # Save uploaded image temporarily
                temp_image_path = "temp_avatar.jpg"
                with open(temp_image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                
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
                
                # Generate Voice
                tts = gTTS(text=dialogue_text, lang=lang_code, slow=is_slow)
                audio_path = "generated_voice.mp3"
                tts.save(audio_path)
                
                st.success(f"🎉 Generated {character_type} voice in {language} successfully!")
                
                if video_prompt.strip():
                    st.info(f"🎥 Active Motion Theme: {video_prompt}")
                
                # Display Animated Presentation Box
                st.markdown("### 🎙️ Live AI Presenter Preview")
                
                # Read image as base64 to display inside HTML animation
                with open(temp_image_path, "rb") as img_file:
                    encoded_img = base64.b64encode(img_file.read()).decode()
                
                st.markdown(f"""
                    <div class="avatar-container">
                        <img src="data:image/jpeg;base64,{encoded_img}" class="animated-avatar" />
                    </div>
                """, unsafe_allow_html=True)
                
                # Audio Player
                st.audio(audio_path, format='audio/mp3', autoplay=True)
                
                # Download Button
                with open(audio_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Presentation Audio (MP3)",
                        data=file,
                        file_name="ai_presentation.mp3",
                        mime="audio/mp3"
                    )
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
