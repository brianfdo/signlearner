# Copy this file to config.py and add your API keys

API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"  # Replace with your YouTube API key

# Vector search configuration
# This token is appended to titles during ingestion and queries during search
# to ensure consistent embedding format and improve similarity matching
# Using a technical delimiter that won't conflict with actual ASL signs
VECTOR_SEARCH_STOP_TOKEN = "##"  # Technical delimiter - never conflicts with real signs 