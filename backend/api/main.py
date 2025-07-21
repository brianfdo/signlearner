# Usage: uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor

from model.llama_client import get_llama_response
from embeddings.embedder import get_embedding
from api.vector_db_utils import query_similar_videos
from config import VECTOR_SEARCH_STOP_TOKEN
from langchain_asl.asl_query_enhancer import get_asl_enhancer
from langchain_asl.lesson_generator import get_lesson_generator

app = FastAPI(title="ASL Learning API", version="1.0.0")

# Initialize ASL query enhancer with LangChain support
# The enhanced asl_query_enhancer now includes LangChain with Llama
asl_enhancer = get_asl_enhancer()
enhancer_type = "LangChain + Llama" if hasattr(asl_enhancer, 'langchain_available') and asl_enhancer.langchain_available else "Rule-based"

# Initialize lesson generator with LangChain support
lesson_generator = get_lesson_generator()

# Performance optimization: Thread pool for parallel processing
_executor = ThreadPoolExecutor(max_workers=4)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str
    fast_mode: Optional[bool] = False

class LessonRequest(BaseModel):
    prompt: str
    age: Optional[int] = None
    experience: Optional[str] = None
    quick_mode: Optional[bool] = False
    ultra_fast: Optional[bool] = False

@app.post("/text-to-asl")
async def text_to_asl(data: TextInput):
    """
    Convert text input to ASL videos with smart phrase-first search strategy
    """
    import time
    start_time = time.time()
    
    try:
        # ✨ ENHANCED: Use ASL query enhancement for better search results (optional)
        if data.fast_mode:
            # Fast mode: skip ASL enhancement for speed
            asl_transformation = type('obj', (object,), {
                'asl_variations': [data.text.lower()],
                'grammar_rules_applied': [],
                'confidence_score': 0.5
            })()
        else:
            # Full mode: use ASL enhancement
            asl_transformation = asl_enhancer.enhance_query(data.text)
        
        # Strategy 1: Try ASL-enhanced phrase searches
        best_phrase_match = None
        best_phrase_similarity = 0
        phrase_search_info = []
        
        # Filter out empty variations and prioritize ASL grammar transformations
        valid_variations = [v for v in asl_transformation.asl_variations if v.strip()]
        
        for i, asl_variation in enumerate(valid_variations[:3]):  # Try top 3 variations
            phrase_query = f"{asl_variation} {VECTOR_SEARCH_STOP_TOKEN}"
            phrase_embedding = get_embedding(phrase_query)
            phrase_results = query_similar_videos(phrase_embedding, top_k=1)
            
            if phrase_results['ids'] and phrase_results['ids'][0]:
                video_id = phrase_results['ids'][0][0]
                title = phrase_results['documents'][0][0]
                metadata = phrase_results['metadatas'][0][0]
                similarity = 1 - phrase_results['distances'][0][0]
                
                phrase_search_info.append({
                    "variation": asl_variation,
                    "similarity": similarity,
                    "video_id": video_id
                })
                
                if similarity > best_phrase_similarity:
                    best_phrase_similarity = similarity
                    best_phrase_match = {
                        "word": data.text.lower(),
                        "video_id": video_id,
                        "title": metadata.get('original_title', title),
                        "enhanced_title": title,
                        "url": metadata['url'],
                        "embed_url": metadata['url'].replace("watch?v=", "embed/"),
                        "duration": metadata['duration'],
                        "similarity_score": similarity,
                        "search_type": "asl_phrase",
                        "asl_variation_used": asl_variation,
                        "grammar_rules": asl_transformation.grammar_rules_applied
                    }
        
        phrase_match = best_phrase_match
        phrase_similarity = best_phrase_similarity
        
        # Strategy 2: Try individual words as fallback
        words = data.text.lower().split()
        word_sequence = []
        total_word_similarity = 0
        found_words = 0
        
        for word in words:
            word_query = f"{word} {VECTOR_SEARCH_STOP_TOKEN}"
            word_embedding = get_embedding(word_query)
            word_results = query_similar_videos(word_embedding, top_k=1)
            
            if word_results['ids'] and word_results['ids'][0]:
                video_id = word_results['ids'][0][0]
                title = word_results['documents'][0][0]
                metadata = word_results['metadatas'][0][0]
                similarity = 1 - word_results['distances'][0][0]
                
                word_sequence.append({
                    "word": word,
                    "video_id": video_id,
                    "title": metadata.get('original_title', title),
                    "enhanced_title": title,
                    "url": metadata['url'],
                    "embed_url": metadata['url'].replace("watch?v=", "embed/"),
                    "duration": metadata['duration'],
                    "similarity_score": similarity,
                    "search_type": "word"
                })
                total_word_similarity += similarity
                found_words += 1
            else:
                word_sequence.append({
                    "word": word,
                    "video_id": None,
                    "title": f"No video found for '{word}'",
                    "enhanced_title": None,
                    "url": None,
                    "embed_url": None,
                    "duration": 0,
                    "similarity_score": 0,
                    "search_type": "word"
                })
        
        # Calculate average similarity for word-based approach
        avg_word_similarity = total_word_similarity / len(words) if words else 0
        
        # Decision logic: Choose the better approach
        # Phrase wins if it has high similarity (>0.7) OR if it's significantly better than words
        phrase_threshold = 0.7
        phrase_advantage_threshold = 0.15  # Phrase needs to be 15% better to override words
        
        # Check if the query contains only function words (English grammar words)
        # These should be transformed to ASL grammar rather than searched directly
        function_words = {
            'is', 'are', 'am', 'was', 'were', 'be', 'being', 'been',
            'a', 'an', 'the', 'do', 'does', 'did', 'have', 'has', 'had',
            'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must'
        }
        
        query_words = set(data.text.lower().split())
        
        # If query is only function words, provide educational feedback
        if query_words.issubset(function_words):
            return {
                "success": True,
                "original_text": data.text,
                "search_strategy": "asl_grammar_education",
                "asl_enhancement": {
                    "enhancer_type": enhancer_type,
                    "variations_tried": [data.text.lower()],
                    "grammar_rules_applied": ["ASL Grammar Education"],
                    "confidence_score": 0.9,
                    "educational_note": f"The words '{data.text}' are English grammar words that don't have direct ASL equivalents. In ASL, these are typically omitted or expressed through facial expressions and body language."
                },
                "phrase_similarity": 0.0,
                "word_avg_similarity": 0.0,
                "video_sequence": [],
                "total_videos": 0,
                "found_videos": 0,
                "educational_feedback": {
                    "message": f"'{data.text}' are English grammar words",
                    "asl_grammar_rule": "English grammar words are typically omitted in ASL",
                    "example": "Instead of 'I am happy', ASL would be 'I happy' with appropriate facial expression",
                    "suggestion": "Try searching for content words like 'happy', 'family', 'eat', etc."
                }
            }
        
        # Check if we have meaningful ASL grammar transformations
        has_asl_grammar = any(
            rule in asl_transformation.grammar_rules_applied 
            for rule in ["ASL Grammar Transformation", "Question Restructuring", "Content Word Extraction"]
        )
        
        use_phrase = (
            phrase_match and 
            phrase_similarity > 0.1 and  # Must have some reasonable match
            (
                has_asl_grammar or  # Prefer ASL grammar transformations
                phrase_similarity > phrase_threshold or  # High confidence phrase match
                phrase_similarity > (avg_word_similarity + phrase_advantage_threshold)  # Significantly better than words
            )
        )
        
        response_time = time.time() - start_time
        
        if use_phrase:
            # Use the phrase match
            return {
                "success": True,
                "original_text": data.text,
                "search_strategy": "asl_phrase",
                "asl_enhancement": {
                    "enhancer_type": enhancer_type,
                    "variations_tried": asl_transformation.asl_variations[:3],
                    "grammar_rules_applied": asl_transformation.grammar_rules_applied,
                    "confidence_score": asl_transformation.confidence_score,
                    "best_variation": phrase_match.get("asl_variation_used") if phrase_match else None
                },
                "phrase_similarity": phrase_similarity,
                "word_avg_similarity": avg_word_similarity,
                "video_sequence": [phrase_match],
                "total_videos": 1,
                "found_videos": 1 if phrase_match and phrase_match["video_id"] else 0,
                "response_time_ms": round(response_time * 1000, 2)
            }
        else:
            # Use individual words
            return {
                "success": True,
                "original_text": data.text,
                "search_strategy": "words", 
                "asl_enhancement": {
                    "enhancer_type": enhancer_type,
                    "variations_tried": asl_transformation.asl_variations[:3],
                    "grammar_rules_applied": asl_transformation.grammar_rules_applied,
                    "confidence_score": asl_transformation.confidence_score,
                    "phrase_not_chosen_reason": f"Phrase similarity ({phrase_similarity:.3f}) not strong enough vs words ({avg_word_similarity:.3f})"
                },
                "phrase_similarity": phrase_similarity,
                "word_avg_similarity": avg_word_similarity,
                "video_sequence": word_sequence,
                "total_videos": len(word_sequence),
                "found_videos": len([v for v in word_sequence if v["video_id"] is not None]),
                "response_time_ms": round(response_time * 1000, 2)
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "video_sequence": []
        }

@app.post("/generate-lesson")
async def generate_lesson(data: LessonRequest):
    """
    Generate a comprehensive, structured ASL lesson plan using LangChain
    """
    import time
    start_time = time.time()
    
    try:
        # Generate sophisticated lesson plan using LangChain
        lesson_plan = lesson_generator.generate_lesson_plan(
            topic=data.prompt,
            age=data.age,
            experience=data.experience,
            quick_mode=data.quick_mode,
            ultra_fast=data.ultra_fast
        )
        
        response_time = time.time() - start_time
        
        return {
            "success": True,
            "lesson_topic": lesson_plan.topic,
            "target_age": lesson_plan.target_age,
            "experience_level": lesson_plan.experience_level,
            "vocabulary_words": lesson_plan.vocabulary_words,
            "lesson_objectives": lesson_plan.lesson_objectives,
            "grammar_focus": lesson_plan.grammar_focus,
            "practice_activities": lesson_plan.practice_activities,
            "cultural_notes": lesson_plan.cultural_notes,
            "difficulty_level": lesson_plan.difficulty_level,
            "estimated_duration": lesson_plan.estimated_duration,
            "lesson_videos": lesson_plan.lesson_videos,
            "total_vocabulary": lesson_plan.total_vocabulary,
            "videos_found": lesson_plan.videos_found,
            "generated_at": lesson_plan.generated_at,
            "langchain_used": hasattr(lesson_generator, 'langchain_available') and lesson_generator.langchain_available,
            "response_time_ms": round(response_time * 1000, 2)
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "lesson_videos": []
        }

@app.get("/")
async def root():
    return {"message": "SignLearner API - Simple ASL Learning Platform"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "endpoints": ["/text-to-asl", "/generate-lesson"],
        "asl_enhancer": enhancer_type,
        "langchain_available": "LangChain" in enhancer_type
    }
