from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
    allow_headers=["*"],
)

WORD_TO_VIDEO = {    
    "hello": "https://www.youtube.com/embed/FVjpLa8GqeM",
    "thank you": "https://www.youtube.com/embed/IvRwNLNR4_w",
    "yes": "https://www.youtube.com/embed/0usayvOXzHo",
    "no": "https://www.youtube.com/embed/QJXKaOSyl4o",
}

class TextInput(BaseModel):
    text: str

@app.post("/text-to-asl")
async def text_to_asl(data: TextInput):
    words = data.text.lower().split()
    video_urls = []
    for word in words:
        video_url = WORD_TO_VIDEO.get(word)
        if video_url:
            video_urls.append(video_url)
    return {"video_sequence": video_urls}

@app.get("/")
async def root():
    return {"message": "Welcome to SignLearner API!"}
