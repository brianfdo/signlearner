"""
LangChain ASL Enhancement Module
===============================

This module provides intelligent ASL query enhancement using both rule-based
and AI-powered transformations to improve search quality for ASL learning.

Core Features:
- ASL grammar transformation (English → ASL structure)
- Multiple search variation generation
- OpenAI integration for advanced transformations
- Transparent rule application tracking

Usage:
    from langchain_asl import get_asl_enhancer
    
    enhancer = get_asl_enhancer()
    result = enhancer.enhance_query("Why does the hotel provide free breakfast?")
"""

from .asl_query_enhancer import get_asl_enhancer, ASLQueryEnhancer, ASLTransformation
from .lesson_generator import get_lesson_generator, ASLLessonGenerator, LessonPlan

__all__ = [
    'get_asl_enhancer', 
    'ASLQueryEnhancer', 
    'ASLTransformation',
    'get_lesson_generator',
    'ASLLessonGenerator', 
    'LessonPlan'
]

__version__ = "1.0.0" 