#!/usr/bin/env python3
"""
ASL Query Enhancement using LangChain
=====================================

This module transforms natural English queries into ASL-friendly search terms
using LangChain with our existing Llama model for intelligent ASL grammar processing.

Key ASL Grammar Rules:
1. Time-Subject-Object-Verb (TSOV) structure
2. Questions end with WH-words (WHO, WHAT, WHERE, WHEN, WHY, HOW)
3. No articles (a, an, the)
4. No copula (to be verbs) in present tense
5. Facial expressions convey grammar
6. Classifiers for spatial relationships
"""

import os
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from functools import lru_cache

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
class ASLTransformation:
    """Result of ASL query transformation"""
    original_query: str
    asl_variations: List[str]
    grammar_rules_applied: List[str]
    confidence_score: float

class ASLQueryEnhancer:
    """
    Enhanced query processor that transforms English to ASL grammar structure
    using LangChain with our existing Llama model
    """
    
    def __init__(self):
        # Initialize LangChain components if available
        self.langchain_available = LANGCHAIN_AVAILABLE
        self.llm = None
        self.asl_chain = None
        
        if self.langchain_available:
            try:
                self.llm = LlamaLangChainWrapper()
                self._setup_langchain_prompts()
            except Exception as e:
                print(f"LangChain setup failed: {e}. Falling back to rule-based.")
                self.langchain_available = False
        
        self.asl_grammar_rules = {
            'remove_articles': ['a', 'an', 'the'],
            'remove_copula': ['is', 'are', 'am', 'was', 'were', 'be', 'being', 'been'],
            'question_words': ['who', 'what', 'where', 'when', 'why', 'how'],
            'time_markers': ['yesterday', 'today', 'tomorrow', 'now', 'later', 'before', 'after', 'morning', 'afternoon', 'evening', 'night'],
            'common_transformations': {
                # English phrase -> ASL equivalent
                'i am': 'me',
                'you are': 'you',
                'he is': 'he',
                'she is': 'she',
                'we are': 'we',
                'they are': 'they',
                'going to': 'will',
                'want to': 'want',
                'need to': 'need',
                'have to': 'must',
                'would like': 'want',
                'how are you': 'you how',
                'what is your name': 'your name what',
                'where are you from': 'you from where',
                'how old are you': 'you age how-much',
                'thank you': 'thank',
                'you\'re welcome': 'welcome',
                'excuse me': 'excuse',
                'i\'m sorry': 'sorry',
                'what time is it': 'time what',
                'how much does it cost': 'cost how-much',
                'where is the bathroom': 'bathroom where',
            }
        }
        
        # Load additional ASL vocabulary mappings
        self.asl_vocabulary = self._load_asl_vocabulary()
    
    def _setup_langchain_prompts(self):
        """Setup LangChain prompts for ASL transformation"""
        asl_prompt_template = PromptTemplate(
            input_variables=["query"],
            template="""You are an expert ASL (American Sign Language) translator and linguist. 
Transform this English query into ASL-friendly search terms that match how signs are actually performed and documented.

ASL Grammar Rules:
1. Focus on CONTENT WORDS (nouns, verbs, adjectives) - these are what get signed
2. Questions end with WH-words (WHAT, WHERE, WHY, HOW, WHO)
3. No articles (a, an, the)
4. No copula verbs (is, are, am) in present tense
5. Subject-Object-Verb or Topic-Comment structure
6. Only include time markers if they are EXPLICITLY mentioned
7. Prioritize the main action and object

Examples:
English: "Why does the hotel provide free breakfast?"
ASL: "HOTEL PROVIDE FREE BREAKFAST WHY?"

English: "What is your name?"
ASL: "YOUR NAME WHAT?"

English: "I am going to the store tomorrow"
ASL: "ME GO STORE" (only include TOMORROW if explicitly mentioned)

English: "Where is the bathroom?"
ASL: "BATHROOM WHERE?"

English: "Where do we go?"
ASL: "WHERE GO" or "GO WHERE"

Transform this English query to ASL format: {query}

IMPORTANT: Focus on the main content words that would be signed. Don't add time markers unless they are explicitly in the query. Provide 3-5 ASL variations, from most ASL-like to simplified versions. Return only the variations, one per line."""
        )
        
        self.asl_chain = LLMChain(llm=self.llm, prompt=asl_prompt_template)
        
    @lru_cache(maxsize=1)
    def _load_asl_vocabulary(self) -> Dict[str, str]:
        """Load common English-to-ASL vocabulary mappings (cached)"""
        return {
            # Common verbs
            'eat': 'eat',
            'drink': 'drink', 
            'sleep': 'sleep',
            'work': 'work',
            'study': 'study',
            'play': 'play',
            'watch': 'watch',
            'listen': 'listen',
            'read': 'read',
            'write': 'write',
            'walk': 'walk',
            'run': 'run',
            'drive': 'drive',
            'fly': 'fly',
            'swim': 'swim',
            'cook': 'cook',
            'clean': 'clean',
            'buy': 'buy',
            'sell': 'sell',
            'help': 'help',
            'teach': 'teach',
            'learn': 'learn',
            
            # Copula verbs (important for ASL learning)
            'is': 'is',
            'are': 'are',
            'am': 'am',
            'was': 'was',
            'were': 'were',
            'be': 'be',
            'being': 'being',
            'been': 'been',
            
            # Family
            'mother': 'mom',
            'father': 'dad',
            'sister': 'sister',
            'brother': 'brother',
            'grandmother': 'grandma',
            'grandfather': 'grandpa',
            'daughter': 'daughter',
            'son': 'son',
            'wife': 'wife',
            'husband': 'husband',
            
            # Common nouns
            'house': 'house',
            'car': 'car',
            'food': 'food',
            'water': 'water',
            'money': 'money',
            'book': 'book',
            'phone': 'phone',
            'computer': 'computer',
            'school': 'school',
            'hospital': 'hospital',
            'restaurant': 'restaurant',
            'store': 'store',
            'hotel': 'hotel',
            'airport': 'airport',
            'train': 'train',
            'bus': 'bus',
            
            # Time expressions
            'morning': 'morning',
            'afternoon': 'afternoon', 
            'evening': 'evening',
            'night': 'night',
            'today': 'today',
            'tomorrow': 'tomorrow',
            'yesterday': 'yesterday',
            
            # Emotions
            'happy': 'happy',
            'sad': 'sad',
            'angry': 'angry',
            'excited': 'excited',
            'tired': 'tired',
            'hungry': 'hungry',
            'thirsty': 'thirsty',
            
            # Colors
            'red': 'red',
            'blue': 'blue',
            'green': 'green',
            'yellow': 'yellow',
            'black': 'black',
            'white': 'white',
            'brown': 'brown',
            'pink': 'pink',
            'purple': 'purple',
            'orange': 'orange',
        }
    
    def enhance_query(self, query: str) -> ASLTransformation:
        """
        Transform English query to ASL-friendly variations
        Using LangChain with Llama for intelligent ASL grammar processing
        """
        original_query = query.strip().lower()
        variations = []
        rules_applied = []
        
        # Strategy 1: LangChain AI-powered transformation (if available)
        if self.langchain_available and self.asl_chain:
            try:
                # Add timeout for LangChain calls using synchronous approach
                import threading
                import queue
                
                result_queue = queue.Queue()
                exception_queue = queue.Queue()
                
                def run_langchain():
                    try:
                        result = self.asl_chain.run(query=original_query)
                        result_queue.put(result)
                    except Exception as e:
                        exception_queue.put(e)
                
                # Run in thread with timeout
                thread = threading.Thread(target=run_langchain)
                thread.daemon = True
                thread.start()
                thread.join(timeout=10.0)  # 10 second timeout
                
                if thread.is_alive():
                    print("LangChain AI transformation timed out, using fallback")
                    # Continue with fallback strategies instead of returning None
                
                if not exception_queue.empty():
                    raise exception_queue.get()
                
                ai_result = result_queue.get()
                
                ai_variations = self._parse_ai_response(ai_result, original_query)
                
                if ai_variations:
                    variations.extend(ai_variations)
                    rules_applied.append("LangChain AI Transformation")
                    print(f"🤖 LangChain AI generated variations: {ai_variations}")
            except Exception as e:
                print(f"LangChain AI transformation failed: {e}")
                # Continue with fallback strategies
        
        # Strategy 2: Rule-based ASL Grammar Transformation
        asl_direct = self._apply_asl_grammar(original_query)
        if asl_direct != original_query and asl_direct.strip():
            variations.append(asl_direct)
            rules_applied.append("ASL Grammar Transformation")
        
        # Strategy 3: Question transformation
        if self._is_question(original_query):
            asl_question = self._transform_question(original_query)
            if asl_question and asl_question not in variations and asl_question.strip():
                variations.append(asl_question)
                rules_applied.append("Question Restructuring")
        
        # Strategy 4: Common phrase substitutions
        asl_phrases = self._apply_common_phrases(original_query)
        if asl_phrases != original_query and asl_phrases not in variations and asl_phrases.strip():
            variations.append(asl_phrases)
            rules_applied.append("Common Phrase Substitution")
        
        # Strategy 5: Content word extraction (remove function words)
        content_words = self._extract_content_words(original_query)
        if content_words != original_query and content_words not in variations and content_words.strip():
            variations.append(content_words)
            rules_applied.append("Content Word Extraction")
        
        # Strategy 6: Vocabulary mapping for remaining words
        asl_vocab = self._apply_vocabulary_mapping(original_query)
        if asl_vocab != original_query and asl_vocab not in variations and asl_vocab.strip():
            variations.append(asl_vocab)
            rules_applied.append("Vocabulary Mapping")
        
        # Remove duplicates while preserving order
        unique_variations = []
        seen = set()
        for var in variations:
            if var.lower() not in seen:
                unique_variations.append(var)
                seen.add(var.lower())
        
        # Only include original if no ASL transformations were successful
        if not unique_variations:
            unique_variations.append(original_query)
        
        # Calculate confidence based on ASL grammar application and LangChain usage
        confidence = min(0.95, len(rules_applied) * 0.3 + 0.2)
        if "LangChain AI Transformation" in rules_applied:
            confidence = min(0.95, confidence + 0.1)  # Boost confidence for AI
        
        return ASLTransformation(
            original_query=query,
            asl_variations=unique_variations,
            grammar_rules_applied=rules_applied,
            confidence_score=confidence
        )
    
    def _apply_asl_grammar(self, query: str) -> str:
        """Apply core ASL grammar rules"""
        words = query.split()
        
        # Special case: If the query is just a single word that's a copula verb,
        # don't remove it - it's likely someone searching for that specific sign
        if len(words) == 1 and words[0] in self.asl_grammar_rules['remove_copula']:
            return query  # Keep the original query unchanged
        
        # Remove articles
        words = [w for w in words if w not in self.asl_grammar_rules['remove_articles']]
        
        # Remove copula verbs in present tense (only in multi-word contexts)
        words = [w for w in words if w not in self.asl_grammar_rules['remove_copula']]
        
        # Handle time markers (move to front)
        time_words = []
        other_words = []
        
        for word in words:
            if word in self.asl_grammar_rules['time_markers']:
                time_words.append(word)
            else:
                other_words.append(word)
        
        # Reconstruct with time first
        result_words = time_words + other_words
        
        return ' '.join(result_words)
    
    def _is_question(self, query: str) -> bool:
        """Check if query is a question"""
        query_lower = query.lower()
        return (
            query.endswith('?') or 
            any(query_lower.startswith(qw) for qw in self.asl_grammar_rules['question_words']) or
            'how are' in query_lower or
            'what is' in query_lower or
            'where is' in query_lower
        )
    
    def _transform_question(self, query: str) -> Optional[str]:
        """Transform English questions to ASL structure"""
        query_clean = query.rstrip('?').lower()
        
        # Apply common question transformations
        for english, asl in self.asl_grammar_rules['common_transformations'].items():
            if english in query_clean:
                return query_clean.replace(english, asl)
        
        # General question word movement
        for qword in self.asl_grammar_rules['question_words']:
            if query_clean.startswith(qword):
                # Move question word to end
                rest = query_clean[len(qword):].strip()
                rest = self._apply_asl_grammar(rest)
                return f"{rest} {qword}" if rest else qword
        
        return None
    
    def _apply_common_phrases(self, query: str) -> str:
        """Apply common phrase transformations"""
        result = query.lower()
        
        for english, asl in self.asl_grammar_rules['common_transformations'].items():
            result = result.replace(english, asl)
        
        return result
    
    def _apply_vocabulary_mapping(self, query: str) -> str:
        """Map English words to ASL vocabulary"""
        words = query.lower().split()
        mapped_words = []
        
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[^\w\s]', '', word)
            mapped_word = self.asl_vocabulary.get(clean_word, clean_word)
            mapped_words.append(mapped_word)
        
        return ' '.join(mapped_words)
    
    def _extract_content_words(self, query: str) -> str:
        """Extract content words for ASL, removing English grammar words"""
        words = query.lower().split()
        
        # ASL function words to remove (English grammar that doesn't exist in ASL)
        asl_function_words = {
            # Articles
            'a', 'an', 'the',
            # Copula verbs (linking verbs)
            'is', 'are', 'am', 'was', 'were', 'be', 'being', 'been',
            # Auxiliary verbs
            'do', 'does', 'did', 'have', 'has', 'had', 'will', 'would', 'could', 'should',
            'can', 'may', 'might', 'must',
            # Prepositions (many are expressed spatially in ASL)
            'to', 'of', 'in', 'on', 'at', 'by', 'for', 'with', 'from', 'up', 'down', 
            'out', 'off', 'over', 'under',
            # Adverbs (often expressed through facial expressions)
            'very', 'really', 'quite', 'rather', 'too', 'so', 'just', 'only',
            # Conjunctions (often omitted in ASL)
            'and', 'or', 'but', 'because', 'if', 'when', 'while',
            # Other function words
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
            'not', 'own', 'same', 'than', 'again', 'further'
        }
        
        # Keep only content words (nouns, verbs, adjectives)
        content_words = []
        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word.lower())
            if clean_word and clean_word not in asl_function_words and len(clean_word) > 1:
                content_words.append(clean_word)
        
        return ' '.join(content_words)
    
    def _parse_ai_response(self, response: str, original_query: str = "") -> List[str]:
        """Parse AI response to extract ASL variations"""
        variations = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Remove numbering (1., 2., etc.)
            line = re.sub(r'^\d+\.\s*', '', line)
            
            # Look for ASL format (often in quotes or after "ASL:")
            if '"' in line:
                # Extract quoted text
                quotes = re.findall(r'"([^"]*)"', line)
                variations.extend(quotes)
            elif 'ASL:' in line:
                # Extract after "ASL:"
                asl_part = line.split('ASL:')[-1].strip()
                if asl_part:
                    variations.append(asl_part)
            elif line.isupper() and len(line.split()) > 1:
                # Looks like ASL format (all caps)
                variations.append(line.lower())
            elif len(line.split()) > 1 and not line.startswith('English:'):
                # General multi-word response
                variations.append(line.lower())
        
        # Filter and clean variations
        cleaned_variations = []
        for v in variations:
            v = v.strip().rstrip('?')
            if v and self._is_good_variation(v, original_query):
                cleaned_variations.append(v)
        
        return cleaned_variations
    
    def _is_good_variation(self, variation: str, original_query: str = "") -> bool:
        """Check if a variation is good for search"""
        # Skip variations that are too generic or contain unwanted time markers
        unwanted_time_markers = ['tomorrow', 'yesterday', 'today', 'morning', 'afternoon', 'evening', 'night']
        
        # If the original query doesn't contain time markers, filter them out
        original_words = set(original_query.split())
        variation_words = set(variation.split())
        
        # Check if variation adds unwanted time markers
        added_time_markers = [word for word in unwanted_time_markers if word in variation_words and word not in original_words]
        if added_time_markers:
            return False
        
        # Skip variations that are too short or too long
        if len(variation.split()) < 1 or len(variation.split()) > 5:
            return False
        
        # Skip variations that are just function words
        function_words = {'is', 'are', 'am', 'was', 'were', 'be', 'being', 'been', 'a', 'an', 'the', 'do', 'does', 'did'}
        if set(variation.split()).issubset(function_words):
            return False
        
        return True

# Factory function for easy integration
def get_asl_enhancer() -> ASLQueryEnhancer:
    """Get configured ASL query enhancer"""
    return ASLQueryEnhancer()

# Test function
def test_asl_enhancements():
    """Test the ASL enhancement system"""
    enhancer = get_asl_enhancer()
    
    test_queries = [
        "Why does the hotel provide free breakfast?",
        "What is your name?", 
        "How are you doing today?",
        "I am going to the store tomorrow",
        "Where is the bathroom?",
        "I love you",
        "Thank you very much",
        "What time is it?",
        "How much does this cost?",
        "I want to learn sign language"
    ]
    
    print("🧠 ASL Query Enhancement Test Results")
    print("=" * 50)
    
    for query in test_queries:
        result = enhancer.enhance_query(query)
        print(f"\n📝 Original: '{result.original_query}'")
        print(f"🎯 ASL Variations:")
        for i, variation in enumerate(result.asl_variations, 1):
            print(f"   {i}. {variation}")
        print(f"🔧 Rules Applied: {', '.join(result.grammar_rules_applied)}")
        print(f"📊 Confidence: {result.confidence_score:.2f}")

if __name__ == "__main__":
    test_asl_enhancements() 