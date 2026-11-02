import streamlit as st
from gtts import gTTS
import os
import requests
import json

st.set_page_config(page_title="AI Talking Video Generator", page_icon="🎥", layout="centered")
st.title("🎬 Professional AI Talking Video Generator")

api_token = "r8_FG00ecw3JqgZADKuF7DEuV3RIQlU5fX1nFD4x"

uploaded_image = st.file_uploader("Upload Avatar Image", type=["png", "jpg", "jpeg"])
dialogue_text = st.text_area("Type dialogue script:")

if st.button("Generate Video"):
    if not uploaded_image:
        st.warning("Please upload an image!")
    else:
        with st.spinner("Generating audio and processing..."):
            # 1. Generate Audio
            tts = gTTS(text=dialogue_text, lang="en")
            audio_path = "voice.mp3"
            tts.save(audio_path)
            st.audio(audio_path)
            
            # 2. Direct HTTP API Call to Replicate
            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json"
            }
            
            # Using Replicate HTTP endpoint
            payload = {
                "version": "9bbef67ad4b63021fb0327f4ca75a40b4353347b749007f3521d96078f4b045e",
                "input": {
                    "motion_bucket_id": 127,
                    "fps": 7
                }
            }
            
            response = requests.post(
                "https://api.replicate.com/v1/predictions", 
                headers=headers, 
                data=json.dumps(payload)
            )
            
            st.write("API Response Status:", response.status_code)
            st.json(response.json())
