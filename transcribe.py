from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def transcribe_audio(path: str):
    with open(path, 'rb') as f:
        res = client.audio.transcriptions.create(model='whisper-1', file=f)
    return res.text

if __name__ == '__main__':
    print(transcribe_audio('voice_message.mp3'))
