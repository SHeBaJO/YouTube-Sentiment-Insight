"""
Emotion detection service using Hugging Face Transformers
"""
import pandas as pd
from transformers import pipeline
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class EmotionService:
    """Service for emotion detection"""
    
    def __init__(self, model_name: str = "j-hartmann/emotion-english-distilroberta-base"):
        """
        Initialize emotion detection model
        
        Args:
            model_name: Hugging Face emotion detection model
        """
        self.model_name = model_name
        self._model = None
    
    @property
    def model(self):
        """Lazy load emotion pipeline"""
        if self._model is None:
            logger.info(f"Loading emotion model: {self.model_name}")
            self._model = pipeline(
                "text-classification",
                model=self.model_name,
                device=-1
            )
        return self._model
    
    def detect_emotion(self, text: str) -> Dict:
        """
        Detect emotion in text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with emotion and score
        """
        try:
            if not text or len(text.strip()) < 3:
                return {"emotion": "neutral", "score": 0.0}
            
            result = self.model(text[:512])[0]
            
            emotion = result["label"].lower()
            score = result["score"]
            
            return {
                "emotion": emotion,
                "score": score
            }
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            return {"emotion": "neutral", "score": 0.0}
    
    def detect_batch(self, texts: List[str], batch_size: int = 32) -> List[Dict]:
        """
        Detect emotions in a batch of texts
        
        Args:
            texts: List of text strings
            batch_size: Number of texts to process at once
            
        Returns:
            List of emotion detection results
        """
        results = []
        try:
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_results = self.model(batch)
                
                for result in batch_results:
                    emotion = result["label"].lower()
                    score = result["score"]
                    
                    results.append({
                        "emotion": emotion,
                        "score": score
                    })
        except Exception as e:
            logger.error(f"Error in batch emotion detection: {e}")
            return [{"emotion": "neutral", "score": 0.0} for _ in texts]
        
        return results
    
    def add_emotion_to_dataframe(self, df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
        """
        Add emotion detection to DataFrame
        
        Args:
            df: Input DataFrame
            text_column: Name of column containing text
            
        Returns:
            DataFrame with added emotion columns
        """
        try:
            df = df.copy()
            texts = df[text_column].fillna("").tolist()
            emotions = self.detect_batch(texts)
            
            df["emotion"] = [e["emotion"] for e in emotions]
            df["emotion_score"] = [e["score"] for e in emotions]
            
            return df
        except Exception as e:
            logger.error(f"Error adding emotion to DataFrame: {e}")
            return df
    
    def get_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Get emotion statistics
        
        Args:
            df: DataFrame with emotion detection
            
        Returns:
            Dictionary with emotion statistics
        """
        try:
            if "emotion" not in df.columns:
                return {}
            
            total = len(df)
            if total == 0:
                return {}
            
            emotion_counts = df["emotion"].value_counts()
            
            stats = {
                "total_comments": total
            }
            
            # Add counts and percentages for each emotion
            emotions = ["joy", "anger", "sadness", "fear", "love", "surprise", "neutral"]
            for emotion in emotions:
                count = int(emotion_counts.get(emotion, 0))
                stats[emotion] = count
                stats[f"{emotion}_percent"] = round((count / total) * 100, 2)
            
            # Get average score
            stats["average_score"] = round(df["emotion_score"].mean(), 3)
            
            return stats
        except Exception as e:
            logger.error(f"Error getting emotion statistics: {e}")
            return {}
    
    def get_dominant_emotions(self, df: pd.DataFrame, limit: int = 5) -> List[Dict]:
        """
        Get dominant emotions
        
        Args:
            df: DataFrame with emotion detection
            limit: Number of emotions to return
            
        Returns:
            List of dominant emotions with counts
        """
        try:
            if "emotion" not in df.columns:
                return []
            
            emotion_counts = df["emotion"].value_counts().head(limit)
            
            result = []
            for emotion, count in emotion_counts.items():
                result.append({
                    "emotion": emotion,
                    "count": int(count),
                    "percentage": round((count / len(df)) * 100, 2)
                })
            
            return result
        except Exception as e:
            logger.error(f"Error getting dominant emotions: {e}")
            return []
