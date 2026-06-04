"""
Sentiment analysis service using Hugging Face Transformers
"""
import pandas as pd
import numpy as np
from transformers import pipeline
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class SentimentService:
    """Service for sentiment analysis"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initialize sentiment analysis model
        
        Args:
            model_name: Hugging Face model name
        """
        self.model_name = model_name
        self._model = None
    
    @property
    def model(self):
        """Lazy load sentiment pipeline"""
        if self._model is None:
            logger.info(f"Loading sentiment model: {self.model_name}")
            self._model = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                device=-1  # CPU only, use device=0 for GPU
            )
        return self._model
    
    def analyze_comment(self, text: str) -> Dict:
        """
        Analyze sentiment of a single comment
        
        Args:
            text: Comment text
            
        Returns:
            Dictionary with sentiment label and score
        """
        try:
            if not text or len(text.strip()) < 3:
                return {"sentiment": "Neutral", "score": 0.0}
            
            result = self.model(text[:512])[0]  # Truncate to 512 tokens max
            
            label = result["label"].lower()
            score = result["score"]
            
            # Normalize labels
            if label == "negative":
                sentiment = "Negative"
            elif label == "positive":
                sentiment = "Positive"
            else:
                sentiment = "Neutral"
            
            return {
                "sentiment": sentiment,
                "score": score
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"sentiment": "Neutral", "score": 0.0}
    
    def analyze_batch(self, texts: List[str], batch_size: int = 32) -> List[Dict]:
        """
        Analyze sentiment for a batch of texts
        
        Args:
            texts: List of text strings
            batch_size: Number of texts to process at once
            
        Returns:
            List of sentiment analysis results
        """
        results = []
        try:
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_results = self.model(batch)
                
                for result in batch_results:
                    label = result["label"].lower()
                    score = result["score"]
                    
                    if label == "negative":
                        sentiment = "Negative"
                    elif label == "positive":
                        sentiment = "Positive"
                    else:
                        sentiment = "Neutral"
                    
                    results.append({
                        "sentiment": sentiment,
                        "score": score
                    })
        except Exception as e:
            logger.error(f"Error in batch analysis: {e}")
            return [{"sentiment": "Neutral", "score": 0.0} for _ in texts]
        
        return results
    
    def add_sentiment_to_dataframe(self, df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
        """
        Add sentiment analysis to DataFrame
        
        Args:
            df: Input DataFrame
            text_column: Name of column containing text
            
        Returns:
            DataFrame with added sentiment columns
        """
        try:
            df = df.copy()
            texts = df[text_column].fillna("").tolist()
            sentiments = self.analyze_batch(texts)
            
            df["sentiment"] = [s["sentiment"] for s in sentiments]
            df["sentiment_score"] = [s["score"] for s in sentiments]
            
            return df
        except Exception as e:
            logger.error(f"Error adding sentiment to DataFrame: {e}")
            return df
    
    def get_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Get sentiment statistics
        
        Args:
            df: DataFrame with sentiment analysis
            
        Returns:
            Dictionary with statistics
        """
        try:
            if "sentiment" not in df.columns:
                return {}
            
            total = len(df)
            if total == 0:
                return {}
            
            sentiment_counts = df["sentiment"].value_counts()
            
            stats = {
                "total_comments": total,
                "positive": int(sentiment_counts.get("Positive", 0)),
                "negative": int(sentiment_counts.get("Negative", 0)),
                "neutral": int(sentiment_counts.get("Neutral", 0)),
                "positive_percent": round((sentiment_counts.get("Positive", 0) / total) * 100, 2),
                "negative_percent": round((sentiment_counts.get("Negative", 0) / total) * 100, 2),
                "neutral_percent": round((sentiment_counts.get("Neutral", 0) / total) * 100, 2),
                "average_score": round(df["sentiment_score"].mean(), 3)
            }
            
            return stats
        except Exception as e:
            logger.error(f"Error getting sentiment statistics: {e}")
            return {}
    
    def get_top_comments(self, df: pd.DataFrame, sentiment: str, limit: int = 5) -> List[Dict]:
        """
        Get top comments by sentiment
        
        Args:
            df: DataFrame with sentiment analysis
            sentiment: "Positive", "Negative", or "Neutral"
            limit: Number of comments to return
            
        Returns:
            List of top comments
        """
        try:
            filtered = df[df["sentiment"] == sentiment].nlargest(limit, "sentiment_score")
            
            comments = []
            for _, row in filtered.iterrows():
                comments.append({
                    "text": row.get("text", ""),
                    "score": round(row.get("sentiment_score", 0), 3),
                    "likes": row.get("likes", 0)
                })
            
            return comments
        except Exception as e:
            logger.error(f"Error getting top comments: {e}")
            return []
