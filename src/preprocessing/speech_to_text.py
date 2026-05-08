import whisper
import os
from moviepy.editor import VideoFileClip

# Load whisper model
model = whisper.load_model("base")


def convert_audio_to_text(audio_path):

    result = model.transcribe(audio_path)

    return result["text"]


def convert_video_to_text(video_path):

    audio_output = "uploads/temp_audio.wav"

    # Extract audio from video
    video = VideoFileClip(video_path)

    video.audio.write_audiofile(audio_output)

    # Convert extracted audio to text
    result = model.transcribe(audio_output)

    # Delete temporary audio file
    if os.path.exists(audio_output):
        os.remove(audio_output)

    return result["text"]