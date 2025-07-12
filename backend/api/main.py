# Usage: uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from model.llama_client import get_llama_response
from embeddings.embedder import get_embedding
from api.vector_db_utils import query_similar_videos
from api.asl_query_processor import ASLQueryProcessor

app = FastAPI()

# Initialize the ASL query processor
asl_processor = ASLQueryProcessor()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST", "GET"],
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

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10

@app.post("/search-videos")
async def search_videos(data: SearchRequest):
    """
    Intelligent ASL video search with LLM preprocessing for better context understanding
    """
    try:
        # Use intelligent preprocessing for better search results
        result = asl_processor.search_with_preprocessing(
            user_input=data.query,
            limit=data.limit or 10
        )
        
        return result
    
    except Exception as e:
        return {"error": str(e), "results": []}

@app.post("/text-to-asl")
async def text_to_asl(data: TextInput):
    """
    Smart text-to-ASL conversion with LLM preprocessing for better context understanding
    """
    try:
        # Use intelligent preprocessing for better ASL translation
        result = asl_processor.smart_text_to_asl(
            text=data.text,
            max_videos=5
        )
        
        return result
    
    except Exception as e:
        return {"error": str(e), "video_sequence": []}

@app.post("/generate-lesson")
async def generate_lesson(data: LessonRequest):
    """
    Generate lesson plan using LLM and RAG search for relevant videos
    """
    try:
        # Use LLM to generate lesson keywords
        llama_prompt = f"""
        You're an ASL learning assistant for children. 
        The user wants to learn: "{data.prompt}". 
        They're {data.age or 'unspecified'} years old with {data.experience or 'beginner'} ASL experience. 
        
        Create a structured lesson plan with:
        1. 5-8 essential ASL signs/words they should learn
        2. Focus on practical, child-friendly vocabulary
        3. Return ONLY the words/phrases separated by commas
        
        Example: hello, thank you, please, more, help, family, happy
        """
        
        keywords_response = get_llama_response(llama_prompt)
        keywords = [word.strip() for word in keywords_response.split(",")]
        
        # Use RAG search to find videos for each keyword
        lesson_videos = []
        for keyword in keywords:
            query_embedding = get_embedding(keyword)
            results = query_similar_videos(query_embedding, top_k=3)
            
            if results['ids'][0]:
                # Get the best match
                video_id = results['ids'][0][0]
                title = results['documents'][0][0]
                metadata = results['metadatas'][0][0]
                similarity = 1 - results['distances'][0][0]
                
                lesson_videos.append({
                    "keyword": keyword,
                    "video_id": video_id,
                    "title": title,
                    "url": metadata['url'],
                    "embed_url": metadata['url'].replace("watch?v=", "embed/"),
                    "duration": metadata['duration'],
                    "similarity_score": similarity
                })
            else:
                lesson_videos.append({
                    "keyword": keyword,
                    "video_id": None,
                    "title": f"No video found for '{keyword}'",
                    "url": None,
                    "embed_url": None,
                    "duration": 0,
                    "similarity_score": 0
                })
        
        return {
            "lesson_plan": lesson_videos,
            "total_videos": len([v for v in lesson_videos if v['video_id'] is not None])
        }
    
    except Exception as e:
        return {"error": str(e), "lesson_plan": []}

@app.post("/smart-search")
async def smart_search(data: SearchRequest):
    """
    Advanced ASL search with detailed preprocessing information
    """
    try:
        result = asl_processor.search_with_preprocessing(
            user_input=data.query,
            limit=data.limit or 10
        )
        
        return {
            "original_query": data.query,
            "preprocessing_analysis": result["preprocessing"],
            "intelligent_results": result["results"],
            "total_found": result["total_found"],
            "improvements": {
                "phrases_detected": len(result["preprocessing"]["phrases_found"]),
                "context_words_identified": len(result["preprocessing"]["analysis"]["context_words"]),
                "enhanced_queries_generated": len(result["preprocessing"]["search_queries"])
            }
        }
    
    except Exception as e:
        return {"error": str(e), "results": []}

@app.get("/")
async def root():
    return {"message": "Welcome to SignLearner API with Intelligent ASL Query Processing!"}
