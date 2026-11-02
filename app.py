import os
import streamlit as st
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip

st.set_page_config(page_title="Free AI Talking Video Generator", page_icon="🎥")

st.title("🎥 Free AI Talking Video Generator")
st.write("Create your talking character videos 100% free without any API tokens or accounts!")

# 1. Text input for speech
text_input = st.text_area("Enter text for your character to speak:", "Hello! Welcome to my AI generated video.")

# 2. Character selection or image upload
character_option = st.selectbox("Choose a Character:", ["Default Avatar", "Custom Image"])

image_path = "default_avatar.jpg"  # Make sure you have a default image or handle uploads

if character_option == "Custom Image":
    uploaded_file = st.file_uploader("Upload character image (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        with open("temp_avatar.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_path = "temp_avatar.jpg"
else:
    # Create a simple placeholder image if default doesn't exist
    if not os.path.exists(image_path):
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (512, 512), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((150, 250), "AI Character", fill=(255, 255, 255))
        img.save(image_path)

# 3. Generate Video Button
if st.button("Generate Talking Video"):
    if not text_input.strip():
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Generating audio and rendering video... Please wait."):
            try:
                # Step A: Generate Audio using gTTS
                audio_file = "output_audio.mp3"
                tts = gTTS(text=text_input, lang='en')
                tts.save(audio_file)
                
                # Step B: Create Video using MoviePy (Combining Image + Audio)
                video_file = "output_video.mp4"
                audio_clip = AudioFileClip(audio_file)
                duration = audio_clip.duration
                
                # Create image clip with the same duration as audio
                image_clip = ImageClip(image_path).set_duration(duration)
                video_clip = image_clip.set_audio(audio_clip)
                
                # Write video file
                video_clip.write_videofile(video_file, fps=24, codec='libx264', audio_codec='aac')
                
                st.success("Video generated successfully!")
                
                # Step C: Display Video & Download Option
                st.video(video_file)
                
                with open(video_file, "rb") as file:
                    st.download_button(
                        label="Download Video",
                        data=file,
                        file_name="ai_talking_video.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")
