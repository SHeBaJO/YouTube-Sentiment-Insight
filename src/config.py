"""
Configuration and environment variables for YouTube Sentiment Analysis
"""
import os
import streamlit as st
from typing import Optional
from dotenv import load_dotenv


load_dotenv()


def get_api_key() -> str:
    """
    Retrieve YouTube API key from environment variables or Streamlit secrets.
    
    Priority:
    1. Streamlit secrets (st.secrets)
    2. Environment variables (os.getenv)
    
    Returns:
        str: YouTube API key
        
    Raises:
        ValueError: If API key is not found
    """
    try:
        # Try Streamlit secrets first
        api_key = st.secrets.get("YOUTUBE_API_KEY")
        if api_key:
            return api_key
    except Exception:
        pass
    
    # Try environment variable
    api_key = os.getenv("YOUTUBE_API_KEY")
    if api_key:
        return api_key
    
    raise ValueError(
        "YOUTUBE_API_KEY not found. Please set it in .streamlit/secrets.toml or as an environment variable."
    )


class Config:
    """Application configuration"""
    
    # API Configuration
    YOUTUBE_API_KEY: str = None
    
    # Model Configuration
    SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
    EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
    MULTILINGUAL_MODEL = "xlm-roberta-base"
    TOPIC_MODEL_MIN_SAMPLES = 3
    TOPIC_MODEL_MIN_CLUSTER_SIZE = 5
    
    # API Request Configuration
    MAX_COMMENTS_DEFAULT = 100
    MAX_COMMENTS_LIMIT = 500
    MIN_COMMENTS = 10
    
    # Analysis Configuration
    CONFIDENCE_THRESHOLD = 0.5
    STOP_WORDS_LANGUAGE = "english"
    
    # Keyword Extraction
    KEYWORD_EXTRACT_METHOD = "tfidf"  # tfidf, rake, textrank
    TOP_KEYWORDS_COUNT = 10
    
    # Export Configuration
    EXPORT_FORMATS = ["CSV", "Excel"]
    
    # Visualization Configuration
    CHART_HEIGHT = 400
    CHART_WIDTH = 800
    
    # Supported Languages
    SUPPORTED_LANGUAGES = [
        "English", "Hindi", "Tamil", "Telugu", "Malayalam",
        "Spanish", "French", "German", "Arabic", "Portuguese"
    ]
    
    def __init__(self):
        """Initialize configuration"""
        try:
            self.YOUTUBE_API_KEY = get_api_key()
        except ValueError as e:
            st.error(f"Configuration Error: {e}")
            raise


# Initialize global config
try:
    config = Config()
except Exception:
    config = None
