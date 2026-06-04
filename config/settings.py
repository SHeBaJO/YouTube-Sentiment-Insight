"""
Configuration and environment variables for YouTube Sentiment Analysis Bot
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # API Configuration
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Model Configuration
    SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
    EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
    MULTILINGUAL_MODEL = "xlm-roberta-base"
    TOPIC_MODEL = "bertopic"  # or "lda"
    
    # Telegram Bot Configuration
    MAX_COMMENT_BATCH = 100
    REQUEST_TIMEOUT = 30
    POLLING_INTERVAL = 60  # seconds
    
    # Analytics Configuration
    DEFAULT_MAX_COMMENTS = 500
    MIN_COMMENT_LENGTH = 3
    KEYWORD_LIMIT = 20
    TOP_COMMENTS_LIMIT = 10
    
    # Report Configuration
    REPORT_FORMATS = ["csv", "xlsx", "pdf"]
    
    # Supported Languages
    SUPPORTED_LANGUAGES = [
        "en", "hi", "ml", "ta", "te", 
        "es", "fr", "de", "ar", "pt"
    ]
    
    @staticmethod
    def validate() -> bool:
        """Validate required configuration"""
        if not Config.YOUTUBE_API_KEY:
            raise ValueError("YOUTUBE_API_KEY environment variable not set")
        if not Config.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
        return True


def get_config() -> Config:
    """Get configuration instance with validation"""
    Config.validate()
    return Config()
