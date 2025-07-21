#!/usr/bin/env python3
"""
Vector Database Utilities for ASL Video Search
=============================================

Optimized utilities for searching ASL videos using vector similarity.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings

# Global thread pool for parallel processing
_executor = ThreadPoolExecutor(max_workers=4)

# Global ChromaDB client for connection pooling
_chroma_client = None

def get_chroma_client():
    """Get ChromaDB client with optimized settings and connection pooling"""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
    return _chroma_client



def query_similar_videos(embedding: List[float], top_k: int = 5) -> Dict[str, Any]:
    """
    Query similar videos using vector similarity
    """
    try:
        client = get_chroma_client()
        collection = client.get_collection("asl_videos")
        
        results = collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=["metadatas", "documents", "distances"]
        )
        
        return {
            'ids': results['ids'],
            'documents': results['documents'],
            'metadatas': results['metadatas'],
            'distances': results['distances']
        }
    except Exception as e:
        print(f"Error querying videos: {e}")
        return {
            'ids': [[]],
            'documents': [[]],
            'metadatas': [[]],
            'distances': [[]]
        }

async def query_videos_parallel(embeddings: List[List[float]], top_k: int = 1) -> List[Dict[str, Any]]:
    """
    Query multiple videos in parallel for better performance
    """
    loop = asyncio.get_event_loop()
    
    # Submit all queries to thread pool
    tasks = [
        loop.run_in_executor(_executor, query_similar_videos, embedding, top_k)
        for embedding in embeddings
    ]
    
    # Wait for all results
    results = await asyncio.gather(*tasks)
    return results

def query_similar_videos_batch(embeddings: List[List[float]], top_k: int = 1) -> List[Dict[str, Any]]:
    """
    Query multiple videos in batch for synchronous operations
    """
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(query_similar_videos, embedding, top_k)
            for embedding in embeddings
        ]
        return [future.result() for future in futures]
