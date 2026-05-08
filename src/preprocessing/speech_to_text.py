import whisper
import subprocess
import os

model = whisper.load_model("base")


def convert_audio_to_text(audio_path):

    try:

        result = model.transcribe(audio_path)

        return result["text"]

    except Exception as e:

        return f"Audio transcription error: {str(e)}"


def convert_video_to_text(video_path):

    audio_output = "uploads/temp_audio.wav"

    try:

        command = [
            "ffmpeg",
            "-i",
            video_path,
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "44100",
            "-ac",
            "2",
            audio_output,
            "-y"
        ]

        subprocess.run(
            command,
            check=True
        )

        result = model.transcribe(audio_output)

        if os.path.exists(audio_output):
            os.remove(audio_output)

        return result["text"]

    except Exception as e:

        return f"Video transcription error: {str(e)}"