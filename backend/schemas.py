"""
SignLearner ASL RAG Application Schemas

Essential data structures for ASL video search and lesson generation.
"""

from typing import List, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class SignCategory(str, Enum):
    """ASL sign categories"""
    GREETINGS = "greetings"
    FAMILY = "family"
    EMOTIONS = "emotions"
    FOOD = "food"
    COLORS = "colors"
    NUMBERS = "numbers"
    ALPHABET = "alphabet"
    ACTIONS = "actions"
    PLACES = "places"
    TIME = "time"
    EVERYDAY = "everyday"


class ASLVideo(BaseModel):
    """ASL video representation"""
    id: str
    title: str
    url: str
    embed_url: str
    duration: float
    thumbnail_url: Optional[str] = None
    category: Optional[SignCategory] = None
    keywords: List[str] = Field(default_factory=list)
    embedding: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.now)


class VideoSearchResult(BaseModel):
    """Video search result with similarity score"""
    video: ASLVideo
    similarity_score: float = Field(..., ge=0, le=1)


class SearchRequest(BaseModel):
    """Video search request"""
    query: str = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=50)
    category_filter: Optional[SignCategory] = None


class LessonGenerationRequest(BaseModel):
    """Lesson generation request"""
    prompt: str
    preferred_duration: int = Field(default=30, ge=5, le=120)
    focus_areas: List[SignCategory] = Field(default_factory=list)


class TextToASLRequest(BaseModel):
    """Text-to-ASL translation request"""
    text: str = Field(..., min_length=1)
    max_videos: int = Field(default=5, ge=1, le=20) 