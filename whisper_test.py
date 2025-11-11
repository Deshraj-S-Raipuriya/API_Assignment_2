# whisper_test.py 

from openai import OpenAI
import os

# Initialize the new client
client = OpenAI(api_key='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')

def transcribe(file_path):
    # Use the new API style for Whisper transcription
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

if __name__ == "__main__":
    txt = transcribe("voice_sample.wav")  # <-- make sure file name matches
    print("Transcription:\n", txt)
