import streamlit as st
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.inference import process_complaint

from src.preprocessing.speech_to_text import (
    convert_audio_to_text,
    convert_video_to_text
)

# Create uploads folder
os.makedirs("uploads", exist_ok=True)

st.title("AI Complaint Auto Routing System")

st.subheader("Enter Complaint Text")

complaint = st.text_area(
    "Type your complaint"
)

st.subheader("Upload Audio File")

audio_file = st.file_uploader(
    "Upload Audio",
    type=["mp3", "wav", "m4a"]
)

st.subheader("Upload Video File")

video_file = st.file_uploader(
    "Upload Video",
    type=["mp4", "mov", "avi"]
)

final_text = complaint

# Audio processing
if audio_file is not None:

    audio_path = os.path.join(
        "uploads",
        audio_file.name
    )

    with open(audio_path, "wb") as f:
        f.write(audio_file.read())

    st.audio(audio_path)

    st.info("Converting audio to text...")

    extracted_text = convert_audio_to_text(
        audio_path
    )

    st.success("Audio converted successfully")

    st.write("Extracted Text:")

    st.write(extracted_text)

    final_text = extracted_text

# Video processing
if video_file is not None:

    video_path = os.path.join(
        "uploads",
        video_file.name
    )

    with open(video_path, "wb") as f:
        f.write(video_file.read())

    st.video(video_path)

    st.info("Converting video speech to text...")

    extracted_text = convert_video_to_text(
        video_path
    )

    st.success("Video converted successfully")

    st.write("Extracted Text:")

    st.write(extracted_text)

    final_text = extracted_text

# Prediction
if st.button("Submit Complaint"):

    if final_text.strip() == "":

        st.error(
            "Please enter complaint or upload file"
        )

    else:

        result = process_complaint(
            final_text
        )

        st.subheader("Prediction Results")

        st.write(
            "Priority:",
            result["priority"]
        )

        st.write(
            "Estimated Resolution Days:",
            result["eta_days"]
        )

        st.write(
            "Assigned Officer:",
            result["assigned_officer"]["name"]
        )

        st.write(
            "Department:",
            result["assigned_officer"]["department"]
        )

        st.subheader("Similar Complaints")

        for case in result["similar_cases"]:

            st.write("-", case)