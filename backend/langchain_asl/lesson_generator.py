#!/usr/bin/env python3
"""
ASL Lesson Plan Generator using LangChain
=========================================

This module generates personalized ASL lesson plans using LangChain with our Llama model.
It creates structured, educational content tailored to the user's needs and experience level.
"""

import re
import json
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

# LangChain integration
try:
    from langchain.llms.base import LLM
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.callbacks.manager import CallbackManagerForLLMRun
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

# Import our existing Llama client
from model.llama_client import get_llama_response

class LlamaLangChainWrapper(LLM):
    """LangChain wrapper for our existing Llama model"""
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None) -> str:
        """Call the Llama model through our existing client"""
        return get_llama_response(prompt)
    
    @property
    def _llm_type(self) -> str:
        return "llama"
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model": "llama3.2"}

@dataclass
class LessonPlan:
    """Structured ASL lesson plan"""
    topic: str
    target_age: Optional[int]
    experience_level: Optional[str]
    vocabulary_words: List[str]
    lesson_objectives: List[str]
    grammar_focus: List[str]
    practice_activities: List[str]
    cultural_notes: List[str]
    difficulty_level: str
    estimated_duration: str
    lesson_videos: List[Dict[str, Any]]
    total_vocabulary: int
    videos_found: int
    generated_at: str

class ASLLessonGenerator:
    """
    Sophisticated ASL lesson plan generator using LangChain
    """
    
    def __init__(self):
        # Initialize LangChain components if available
        self.langchain_available = LANGCHAIN_AVAILABLE
        self.llm = None
        self.lesson_chain = None
        self.vocabulary_chain = None
        
        # Performance optimizations
        self._executor = ThreadPoolExecutor(max_workers=2)
        self._vocabulary_cache = {}
        
        if self.langchain_available:
            try:
                self.llm = LlamaLangChainWrapper()
                self._setup_langchain_prompts()
            except Exception as e:
                print(f"LangChain setup failed: {e}. Falling back to rule-based.")
                self.langchain_available = False
    
    def _setup_langchain_prompts(self):
        """Setup LangChain prompts for lesson generation"""
        
        # Main lesson plan prompt
        lesson_prompt_template = PromptTemplate(
            input_variables=["topic", "age", "experience", "vocabulary"],
            template="""You are an expert ASL (American Sign Language) instructor and curriculum designer.

Create a comprehensive, structured lesson plan for ASL learning.

TOPIC: {topic}
TARGET AGE: {age}
EXPERIENCE LEVEL: {experience}
VOCABULARY WORDS: {vocabulary}

Generate a JSON response with the following structure:
{{
    "lesson_objectives": [
        "Clear, measurable learning goals (2-3 objectives)"
    ],
    "grammar_focus": [
        "Specific ASL grammar concepts to teach (2-3 concepts)"
    ],
    "practice_activities": [
        "Interactive practice activities (3-4 activities)"
    ],
    "cultural_notes": [
        "Important cultural context and notes (2-3 notes)"
    ],
    "difficulty_level": "beginner/intermediate/advanced",
    "estimated_duration": "X minutes"
}}

Focus on:
- Age-appropriate content
- Progressive skill building
- Cultural sensitivity
- Practical application
- Clear, actionable activities

Return ONLY the JSON response, no additional text."""
        )
        
        # Vocabulary generation prompt
        vocabulary_prompt_template = PromptTemplate(
            input_variables=["topic", "age", "experience"],
            template="""You are an expert ASL instructor creating vocabulary lists for lessons.

TOPIC: {topic}
TARGET AGE: {age}
EXPERIENCE LEVEL: {experience}

Generate exactly 6-8 essential ASL vocabulary words for this topic.
Focus on:
- Practical, everyday signs
- Age-appropriate complexity
- Progressive difficulty
- Cultural relevance

Return ONLY a comma-separated list of vocabulary words, nothing else.
Example format: hello, thank you, please, more, help, family

Vocabulary words:"""
        )
        
        self.lesson_chain = LLMChain(llm=self.llm, prompt=lesson_prompt_template)
        self.vocabulary_chain = LLMChain(llm=self.llm, prompt=vocabulary_prompt_template)
    
    def generate_lesson_plan(self, topic: str, age: Optional[int] = None, 
                           experience: Optional[str] = None, quick_mode: bool = False, 
                           ultra_fast: bool = False) -> LessonPlan:
        """
        Generate a comprehensive ASL lesson plan with timeout protection
        """
        import threading
        import queue
        
        result_queue = queue.Queue()
        exception_queue = queue.Queue()
        
        def generate_lesson():
            try:
                # Step 1: Generate vocabulary words
                if ultra_fast:
                    vocabulary_words = self._generate_fallback_vocabulary(topic)
                    print("Ultra-fast mode: Using fallback vocabulary")
                else:
                    vocabulary_words = self._generate_vocabulary(topic, age, experience)
                
                # Step 2: Generate detailed lesson plan
                if ultra_fast:
                    lesson_data = self._generate_fallback_lesson_structure(topic, vocabulary_words)
                    print("Ultra-fast mode: Using fallback lesson structure")
                else:
                    lesson_data = self._generate_lesson_structure(topic, age, experience, vocabulary_words)
                
                # Step 3: Find videos for vocabulary words (with timeout)
                if quick_mode or ultra_fast:
                    # Skip video search for faster response
                    lesson_videos = []
                    print("Fast mode: Skipping video search")
                else:
                    try:
                        lesson_videos = self._find_videos_for_vocabulary(vocabulary_words)
                    except Exception as e:
                        print(f"Video search failed: {e}, using empty videos")
                        lesson_videos = []
                
                # Step 4: Create structured lesson plan
                lesson_plan = LessonPlan(
                    topic=topic,
                    target_age=age,
                    experience_level=experience,
                    vocabulary_words=vocabulary_words,
                    lesson_objectives=lesson_data.get("lesson_objectives", []),
                    grammar_focus=lesson_data.get("grammar_focus", []),
                    practice_activities=lesson_data.get("practice_activities", []),
                    cultural_notes=lesson_data.get("cultural_notes", []),
                    difficulty_level=lesson_data.get("difficulty_level", "beginner"),
                    estimated_duration=lesson_data.get("estimated_duration", "30 minutes"),
                    lesson_videos=lesson_videos,
                    total_vocabulary=len(vocabulary_words),
                    videos_found=len([v for v in lesson_videos if v['video_id'] is not None]),
                    generated_at=datetime.now().isoformat()
                )
                
                result_queue.put(lesson_plan)
            except Exception as e:
                exception_queue.put(e)
        
        # Run lesson generation with timeout
        thread = threading.Thread(target=generate_lesson)
        thread.daemon = True
        thread.start()
        thread.join(timeout=30.0)  # 30 second timeout
        
        if thread.is_alive():
            print("Lesson generation timed out, using fallback")
            return self._create_fallback_lesson(topic, age, experience)
        
        if not exception_queue.empty():
            exception = exception_queue.get()
            print(f"Lesson generation failed: {exception}")
            return self._create_fallback_lesson(topic, age, experience)
        
        return result_queue.get()
    
    def _generate_vocabulary(self, topic: str, age: Optional[int], 
                           experience: Optional[str]) -> List[str]:
        """Generate vocabulary words using LangChain"""
        if self.langchain_available and self.vocabulary_chain:
            try:
                age_str = str(age) if age else "general"
                experience_str = experience or "beginner"
                
                response = self.vocabulary_chain.run(
                    topic=topic,
                    age=age_str,
                    experience=experience_str
                )
                
                vocabulary_words = self._parse_vocabulary_response(response)
                print(f"🤖 LangChain generated vocabulary: {vocabulary_words}")
                return vocabulary_words
                
            except Exception as e:
                print(f"LangChain vocabulary generation failed: {e}")
        
        # Fallback to rule-based vocabulary
        return self._generate_fallback_vocabulary(topic)
    
    def _generate_lesson_structure(self, topic: str, age: Optional[int], 
                                 experience: Optional[str], vocabulary: List[str]) -> Dict[str, Any]:
        """Generate detailed lesson structure using LangChain"""
        if self.langchain_available and self.lesson_chain:
            try:
                age_str = str(age) if age else "general"
                experience_str = experience or "beginner"
                vocabulary_str = ", ".join(vocabulary)
                
                response = self.lesson_chain.run(
                    topic=topic,
                    age=age_str,
                    experience=experience_str,
                    vocabulary=vocabulary_str
                )
                
                lesson_data = self._parse_lesson_response(response)
                print(f"🤖 LangChain generated lesson structure")
                return lesson_data
                
            except Exception as e:
                print(f"LangChain lesson generation failed: {e}")
        
        # Fallback to basic lesson structure
        return self._generate_fallback_lesson_structure(topic, vocabulary)
    
    def _parse_vocabulary_response(self, response: str) -> List[str]:
        """Parse vocabulary response from LangChain"""
        vocabulary_words = []
        cleaned_response = response.strip().lower()
        
        # Remove common prefixes
        prefixes = ['vocabulary:', 'words:', 'signs:', 'asl:', 'vocabulary words:']
        for prefix in prefixes:
            if cleaned_response.startswith(prefix):
                cleaned_response = cleaned_response[len(prefix):].strip()
        
        # Split by commas and clean each word
        raw_words = cleaned_response.split(',')
        for word in raw_words:
            clean_word = word.strip()
            clean_word = re.sub(r'^\d+\.\s*', '', clean_word)  # Remove numbering
            clean_word = clean_word.strip('"\'[](){}')  # Remove quotes/brackets
            clean_word = clean_word.lstrip('•-*')  # Remove bullets
            
            if clean_word and len(clean_word) > 1:
                vocabulary_words.append(clean_word)
        
        # Limit to 8 words maximum
        return vocabulary_words[:8]
    
    def _parse_lesson_response(self, response: str) -> Dict[str, Any]:
        """Parse lesson response from LangChain"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                lesson_json = json_match.group(0)
                return json.loads(lesson_json)
        except Exception as e:
            print(f"Failed to parse lesson JSON: {e}")
        
        # Return fallback structure
        return {
            "lesson_objectives": ["Learn basic ASL vocabulary", "Practice signing"],
            "grammar_focus": ["Basic ASL structure"],
            "practice_activities": ["Practice with partner", "Watch and repeat"],
            "cultural_notes": ["ASL is a complete language"],
            "difficulty_level": "beginner",
            "estimated_duration": "30 minutes"
        }
    
    def _find_videos_for_vocabulary(self, vocabulary_words: List[str]) -> List[Dict[str, Any]]:
        """Find videos for each vocabulary word using optimized parallel processing"""
        from embeddings.embedder import get_embedding
        from api.vector_db_utils import query_similar_videos_batch
        from config import VECTOR_SEARCH_STOP_TOKEN
        
        # Limit vocabulary words to reduce processing time
        max_vocabulary = 4  # Limit to 4 words for faster processing
        vocabulary_words = vocabulary_words[:max_vocabulary]
        
        # Generate all embeddings in parallel
        queries = [f"{word} {VECTOR_SEARCH_STOP_TOKEN}" for word in vocabulary_words]
        
        # Get embeddings in parallel using synchronous approach
        embeddings = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            embedding_futures = [
                executor.submit(get_embedding, query)
                for query in queries
            ]
            embeddings = [future.result() for future in embedding_futures]
        
        # Query videos in batch
        results = query_similar_videos_batch(embeddings, top_k=1)
        
        lesson_videos = []
        for i, (word, result) in enumerate(zip(vocabulary_words, results)):
            if result['ids'][0]:
                video_id = result['ids'][0][0]
                title = result['documents'][0][0]
                metadata = result['metadatas'][0][0]
                similarity = 1 - result['distances'][0][0]
                
                lesson_videos.append({
                    "vocabulary_word": word,
                    "video_id": video_id,
                    "title": metadata.get('original_title', title),
                    "enhanced_title": title,
                    "url": metadata['url'],
                    "embed_url": metadata['url'].replace("watch?v=", "embed/"),
                    "duration": metadata['duration'],
                    "similarity_score": similarity
                })
            else:
                lesson_videos.append({
                    "vocabulary_word": word,
                    "video_id": None,
                    "title": f"No video found for '{word}'",
                    "enhanced_title": None,
                    "url": None,
                    "embed_url": None,
                    "duration": 0,
                    "similarity_score": 0
                })
        
        return lesson_videos
    
    def _generate_fallback_vocabulary(self, topic: str) -> List[str]:
        """Generate fallback vocabulary based on topic"""
        # Basic vocabulary based on common topics
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['family', 'family members']):
            return ['mother', 'father', 'sister', 'brother', 'grandmother', 'grandfather']
        elif any(word in topic_lower for word in ['food', 'eat', 'hungry']):
            return ['eat', 'food', 'hungry', 'thirsty', 'water', 'bread', 'milk']
        elif any(word in topic_lower for word in ['colors', 'color']):
            return ['red', 'blue', 'green', 'yellow', 'black', 'white', 'pink']
        elif any(word in topic_lower for word in ['numbers', 'count']):
            return ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
        elif any(word in topic_lower for word in ['greetings', 'hello']):
            return ['hello', 'goodbye', 'thank you', 'please', 'sorry', 'excuse me']
        else:
            # Generic vocabulary
            return ['hello', 'thank you', 'please', 'more', 'help', 'family']
    
    def _generate_fallback_lesson_structure(self, topic: str, vocabulary: List[str]) -> Dict[str, Any]:
        """Generate fallback lesson structure"""
        return {
            "lesson_objectives": [
                f"Learn ASL vocabulary related to {topic}",
                "Practice basic ASL grammar and structure",
                "Develop signing confidence through practice"
            ],
            "grammar_focus": [
                "Basic ASL sentence structure",
                "Facial expressions in ASL",
                "Non-manual markers"
            ],
            "practice_activities": [
                "Watch and repeat vocabulary videos",
                "Practice signing with a partner",
                "Create simple sentences using new vocabulary"
            ],
            "cultural_notes": [
                "ASL is a complete, natural language",
                "Deaf culture values visual communication",
                "Facial expressions are grammatical in ASL"
            ],
            "difficulty_level": "beginner",
            "estimated_duration": "30 minutes"
        }
    
    def _create_fallback_lesson(self, topic: str, age: Optional[int], 
                              experience: Optional[str]) -> LessonPlan:
        """Create a basic fallback lesson plan"""
        vocabulary_words = self._generate_fallback_vocabulary(topic)
        lesson_structure = self._generate_fallback_lesson_structure(topic, vocabulary_words)
        lesson_videos = self._find_videos_for_vocabulary(vocabulary_words)
        
        return LessonPlan(
            topic=topic,
            target_age=age,
            experience_level=experience,
            vocabulary_words=vocabulary_words,
            lesson_objectives=lesson_structure["lesson_objectives"],
            grammar_focus=lesson_structure["grammar_focus"],
            practice_activities=lesson_structure["practice_activities"],
            cultural_notes=lesson_structure["cultural_notes"],
            difficulty_level=lesson_structure["difficulty_level"],
            estimated_duration=lesson_structure["estimated_duration"],
            lesson_videos=lesson_videos,
            total_vocabulary=len(vocabulary_words),
            videos_found=len([v for v in lesson_videos if v['video_id'] is not None]),
            generated_at=datetime.now().isoformat()
        )

# Factory function for easy integration
def get_lesson_generator() -> ASLLessonGenerator:
    """Get an instance of the ASL lesson generator"""
    return ASLLessonGenerator() 