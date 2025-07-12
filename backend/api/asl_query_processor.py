"""
ASL Query Processor using LangChain for intelligent preprocessing

This module handles the preprocessing of user queries to improve vector database
searches by understanding ASL-specific context and linguistic patterns.
"""

from typing import List, Dict, Any, Optional
from model.llama_client import get_llama_response
from embeddings.embedder import get_embedding
from api.vector_db_utils import query_similar_videos


class ASLQueryProcessor:
    """
    Processes user queries with ASL-specific understanding before vector search
    """
    
    def __init__(self):
        # Common ASL phrase patterns that should be kept together
        self.asl_phrases = {
            "hello there": "greeting with emphasis",
            "thank you": "gratitude expression", 
            "how are you": "greeting question",
            "nice to meet you": "introduction phrase",
            "see you later": "goodbye phrase",
            "what is your name": "introduction question",
            "i love you": "affection expression",
            "good morning": "morning greeting",
            "good night": "evening farewell"
        }
        
        # Words that need disambiguation in ASL context
        self.disambiguation_needed = {
            "i": "first person pronoun - distinct from 'it'",
            "you": "second person pronoun - distinct from 'your'", 
            "it": "third person pronoun - distinct from 'i'",
            "there": "location indicator - context dependent",
            "here": "location indicator - context dependent",
            "this": "demonstrative - requires visual context",
            "that": "demonstrative - requires visual context"
        }

    def preprocess_query(self, user_input: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Preprocess user query using LLM to understand ASL context
        """
        # Step 1: Check for known ASL phrases
        phrases_found = self._extract_asl_phrases(user_input.lower())
        
        # Step 2: Use LLM to analyze and improve the query
        analysis = self._analyze_with_llm(user_input, context, phrases_found)
        
        # Step 3: Generate optimized search queries
        search_queries = self._generate_search_queries(analysis)
        
        return {
            "original_query": user_input,
            "analysis": analysis,
            "search_queries": search_queries,
            "phrases_found": phrases_found
        }

    def _extract_asl_phrases(self, text: str) -> List[Dict[str, str]]:
        """Extract known ASL phrases from text"""
        phrases = []
        for phrase, description in self.asl_phrases.items():
            if phrase in text:
                phrases.append({
                    "phrase": phrase,
                    "description": description,
                    "keep_together": True
                })
        return phrases

    def _analyze_with_llm(self, user_input: str, context: Optional[str], phrases_found: List[Dict]) -> Dict[str, Any]:
        """Use LLM to analyze user input for ASL-specific understanding"""
        
        prompt = f"""
        You are an ASL (American Sign Language) learning assistant. Analyze this user input for ASL learning context:

        User Input: "{user_input}"
        Context: {context or "None provided"}
        Known ASL Phrases Found: {[p['phrase'] for p in phrases_found]}

        Please analyze and provide:
        1. Intent: What does the user want to learn? (translate, practice, lesson, etc.)
        2. Key Signs: What are the most important ASL signs/concepts to focus on?
        3. Contextual Meaning: Any words that need special ASL context consideration?
        4. Search Strategy: How should we search the video database most effectively?

        Respond in this exact format:
        INTENT: [translation/practice/lesson/search]
        KEY_SIGNS: [comma-separated list of important ASL signs]
        CONTEXT_WORDS: [words that need disambiguation in ASL]
        SEARCH_STRATEGY: [brief description of search approach]
        """
        
        response = get_llama_response(prompt)
        return self._parse_llm_response(response)

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse structured LLM response"""
        analysis = {
            "intent": "search",
            "key_signs": [],
            "context_words": [],
            "search_strategy": "direct search"
        }
        
        lines = response.strip().split('\n')
        for line in lines:
            if line.startswith('INTENT:'):
                analysis['intent'] = line.replace('INTENT:', '').strip().lower()
            elif line.startswith('KEY_SIGNS:'):
                signs = line.replace('KEY_SIGNS:', '').strip()
                analysis['key_signs'] = [s.strip() for s in signs.split(',') if s.strip()]
            elif line.startswith('CONTEXT_WORDS:'):
                words = line.replace('CONTEXT_WORDS:', '').strip()
                analysis['context_words'] = [w.strip() for w in words.split(',') if w.strip()]
            elif line.startswith('SEARCH_STRATEGY:'):
                analysis['search_strategy'] = line.replace('SEARCH_STRATEGY:', '').strip()
        
        return analysis

    def _generate_search_queries(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate optimized search queries based on analysis"""
        queries = []
        
        # Primary queries from key signs
        for sign in analysis['key_signs']:
            # Add ASL-specific context to the query
            enhanced_query = self._enhance_query_for_asl(sign, analysis['context_words'])
            queries.append({
                "query": enhanced_query,
                "type": "primary",
                "original_term": sign,
                "weight": 1.0
            })
        
        # Secondary queries for context words
        for word in analysis['context_words']:
            if word in self.disambiguation_needed:
                context_query = f"{word} {self.disambiguation_needed[word]}"
                queries.append({
                    "query": context_query,
                    "type": "context",
                    "original_term": word,
                    "weight": 0.7
                })
        
        return queries

    def _enhance_query_for_asl(self, term: str, context_words: List[str]) -> str:
        """Enhance query with ASL-specific context"""
        # Add ASL-specific terms to improve search
        if term in context_words:
            return f"ASL sign {term} American Sign Language"
        return f"{term} ASL sign"

    def search_with_preprocessing(self, user_input: str, limit: int = 10, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform intelligent search using preprocessing
        """
        # Preprocess the query
        processed = self.preprocess_query(user_input, context)
        
        # Execute searches for all generated queries
        all_results = []
        for query_info in processed['search_queries']:
            query_embedding = get_embedding(query_info['query'])
            results = query_similar_videos(query_embedding, top_k=limit)
            
            # Process results with weight and context
            for i, (video_id, title, metadata, distance) in enumerate(zip(
                results['ids'][0], 
                results['documents'][0], 
                results['metadatas'][0], 
                results['distances'][0]
            )):
                similarity_score = (1 - distance) * query_info['weight']
                
                all_results.append({
                    "id": video_id,
                    "title": title,
                    "url": metadata['url'],
                    "embed_url": metadata['url'].replace("watch?v=", "embed/"),
                    "duration": metadata['duration'],
                    "similarity_score": similarity_score,
                    "query_type": query_info['type'],
                    "matched_term": query_info['original_term'],
                    "search_query": query_info['query']
                })
        
        # Remove duplicates and sort by similarity
        unique_results = {}
        for result in all_results:
            if result['id'] not in unique_results or result['similarity_score'] > unique_results[result['id']]['similarity_score']:
                unique_results[result['id']] = result
        
        final_results = list(unique_results.values())
        final_results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return {
            "query": user_input,
            "preprocessing": processed,
            "results": final_results[:limit],
            "total_found": len(final_results)
        }

    def smart_text_to_asl(self, text: str, max_videos: int = 5) -> Dict[str, Any]:
        """
        Convert text to ASL with intelligent preprocessing
        """
        processed = self.preprocess_query(text)
        
        if processed['phrases_found']:
            # Handle as phrases
            video_sequence = []
            for phrase_info in processed['phrases_found']:
                phrase_query = f"{phrase_info['phrase']} ASL sign"
                query_embedding = get_embedding(phrase_query)
                results = query_similar_videos(query_embedding, top_k=1)
                
                if results['ids'][0]:
                    video_id = results['ids'][0][0]
                    title = results['documents'][0][0]
                    metadata = results['metadatas'][0][0]
                    
                    video_sequence.append({
                        "phrase": phrase_info['phrase'],
                        "video_url": metadata['url'].replace("watch?v=", "embed/"),
                        "video_title": title,
                        "source": "phrase_search",
                        "description": phrase_info['description']
                    })
            
            return {
                "video_sequence": video_sequence,
                "processing_type": "phrase_based",
                "preprocessing": processed
            }
        else:
            # Handle as individual words with context
            video_sequence = []
            for sign in processed['analysis']['key_signs'][:max_videos]:
                enhanced_query = self._enhance_query_for_asl(sign, processed['analysis']['context_words'])
                query_embedding = get_embedding(enhanced_query)
                results = query_similar_videos(query_embedding, top_k=1)
                
                if results['ids'][0]:
                    video_id = results['ids'][0][0]
                    title = results['documents'][0][0]
                    metadata = results['metadatas'][0][0]
                    
                    video_sequence.append({
                        "word": sign,
                        "video_url": metadata['url'].replace("watch?v=", "embed/"),
                        "video_title": title,
                        "source": "smart_search",
                        "enhanced_query": enhanced_query
                    })
            
            return {
                "video_sequence": video_sequence,
                "processing_type": "word_based",
                "preprocessing": processed
            } 