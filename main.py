from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# HF_API_KEY = os.getenv('HF_API_KEY')



class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post('/chat')
async def chat_endpoint(req: ChatRequest):
    # simple relay to OpenAI Chat Completion API
    import openai
    openai.api_key = OPENAI_API_KEY
    resp = openai.ChatCompletion.create(        
        model='gpt-5-pretty-spry',# #model='gpt-4o-mini', 
        messages=[
            {'role': 'system', 'content': 'You are a helpful customer support assistant.'},
            {'role': 'user', 'content': req.message}
        ],
        max_tokens=300
    )
    answer = resp['choices'][0]['message']['content']
    return {'answer': answer}

@app.post('/upload_screenshot')
async def upload_screenshot(file: UploadFile = File(...)):
    # save temporarily and call CV model
    contents = await file.read()
    tmp_path = f'/tmp/{file.filename}'
    with open(tmp_path, 'wb') as f:
        f.write(contents)
    # Here we'd call a CV service; for demo return placeholder
    return {'status': 'received', 'filename': file.filename}
