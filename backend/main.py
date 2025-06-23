from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from llama_client import get_llama_response

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

class LessonRequest(BaseModel):
    prompt: str
    age: Optional[int] = None
    experience: Optional[str] = None

@app.post("/text-to-asl")
async def text_to_asl(data: TextInput):
    words = data.text.lower().split()
    video_urls = []
    for word in words:
        video_url = WORD_TO_VIDEO.get(word)
        if video_url:
            video_urls.append(video_url)
    return {"video_sequence": video_urls}

@app.post("/generate-lesson")
async def generate_lesson(data: LessonRequest):
    llama_prompt = f"""
    You're an ASL learning assistant. 
    The user wants to learn: "{data.prompt}". 
    They're {data.age} years old with {data.experience} ASL experience. 
    Recommend 5 ASL keywords or phrases they should learn.
    Provide them as a comma-separated list.
    """
    keywords = get_llama_response(llama_prompt)
    keyword_list = [word.strip() for word in keywords.split(",")]
    
    video_urls = []
    for word in keyword_list:
        video_url = WORD_TO_VIDEO.get(word.lower())
        if video_url:
            video_urls.append({"word": word, "video_url": video_url})
        else:
            video_urls.append({"word": word, "video_url": None})

    return {"video_sequence": video_urls}

@app.get("/")
async def root():
    return {"message": "Welcome to SignLearner API!"}
