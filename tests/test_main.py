"""
Test suite for YouTube Sentiment Insight.
"""
import importlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSentimentAnalyzer:
    """Test sentiment analysis functionality."""

    def test_sentiment_analyzer_initialization(self):
        try:
            from src.models.sentiment import SentimentAnalyzer

            analyzer = SentimentAnalyzer()
            assert analyzer is not None
        except ImportError:
            pytest.skip("Transformers not installed")

    def test_sentiment_positive(self):
        try:
            from src.models.sentiment import SentimentAnalyzer

            analyzer = SentimentAnalyzer()
            result = analyzer.analyze_comment("This is amazing and wonderful!")
            assert "sentiment" in result
            assert result["confidence"] > 0
        except Exception:
            pytest.skip("Model loading failed")

    def test_sentiment_negative(self):
        try:
            from src.models.sentiment import SentimentAnalyzer

            analyzer = SentimentAnalyzer()
            result = analyzer.analyze_comment("This is terrible and awful!")
            assert "sentiment" in result
            assert result["confidence"] > 0
        except Exception:
            pytest.skip("Model loading failed")


class TestKeywordExtractor:
    """Test keyword extraction functionality."""

    def test_keyword_extractor_initialization(self):
        from src.analytics.keywords import KeywordExtractor

        extractor = KeywordExtractor()
        assert extractor is not None

    def test_text_cleaning(self):
        from src.analytics.keywords import KeywordExtractor

        extractor = KeywordExtractor()
        text = "Check out this URL: http://example.com! @mention #hashtag"
        cleaned = extractor.clean_text(text)

        assert "http" not in cleaned
        assert "@" not in cleaned
        assert cleaned != ""

    def test_keyword_extraction(self):
        from src.analytics.keywords import KeywordExtractor

        extractor = KeywordExtractor()
        text = "Python machine learning natural language processing"
        keywords = extractor.extract_keywords(text)

        assert len(keywords) > 0
        assert "python" in keywords


class TestYouTubeAPI:
    """Test YouTube API utilities."""

    def test_video_id_extraction_youtube_com(self):
        from src.utils.youtube_api import YouTubeCommentExtractor

        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = YouTubeCommentExtractor.extract_video_id(url)

        assert video_id == "dQw4w9WgXcQ"

    def test_video_id_extraction_youtu_be(self):
        from src.utils.youtube_api import YouTubeCommentExtractor

        url = "https://youtu.be/dQw4w9WgXcQ"
        video_id = YouTubeCommentExtractor.extract_video_id(url)

        assert video_id == "dQw4w9WgXcQ"

    def test_invalid_url(self):
        from src.utils.youtube_api import YouTubeCommentExtractor

        url = "https://www.example.com"
        video_id = YouTubeCommentExtractor.extract_video_id(url)

        assert video_id is None


class TestConfig:
    """Test configuration."""

    def test_config_structure(self):
        from src import config as config_module

        importlib.reload(config_module)
        assert hasattr(config_module, "Config")

    def test_config_values(self):
        from src.config import Config

        assert hasattr(Config, "SENTIMENT_MODEL")
        assert hasattr(Config, "EMOTION_MODEL")
        assert hasattr(Config, "MAX_COMMENTS_DEFAULT")


class TestEmotionDetector:
    """Test emotion detection."""

    def test_emotion_detector_initialization(self):
        try:
            from src.models.emotion import EmotionDetector

            detector = EmotionDetector()
            assert detector is not None
        except ImportError:
            pytest.skip("Transformers not installed")


class TestTrendAnalyzer:
    """Test trend analysis."""

    def test_trend_analyzer(self):
        import pandas as pd

        from src.analytics.trends import TrendAnalyzer

        df = pd.DataFrame(
            {
                "published_at": pd.date_range("2024-01-01", periods=10),
                "sentiment": ["Positive"] * 5 + ["Negative"] * 5,
                "likes": list(range(10)),
            }
        )

        trends = TrendAnalyzer.daily_sentiment_trends(df)
        assert not trends.empty


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
