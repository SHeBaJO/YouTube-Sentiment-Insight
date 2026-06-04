"""
Topic modeling service using BERTopic
"""
import pandas as pd
from typing import List, Dict, Optional
import logging
import numpy as np

logger = logging.getLogger(__name__)

try:
    from bertopic import BERTopic
    BERTOPIC_AVAILABLE = True
except ImportError:
    BERTOPIC_AVAILABLE = False
    logger.warning("BERTopic not available. Topic modeling will be limited.")


class TopicService:
    """Service for topic modeling and analysis"""
    
    def __init__(self):
        """Initialize topic service"""
        self.model = None
        if BERTOPIC_AVAILABLE:
            self._initialize_model()
    
    def _initialize_model(self):
        """Initialize BERTopic model"""
        try:
            self.model = BERTopic(language="english", calculate_probabilities=True)
            logger.info("BERTopic model initialized")
        except Exception as e:
            logger.error(f"Error initializing BERTopic: {e}")
            self.model = None
    
    def extract_topics(self, texts: List[str], num_topics: int = 5) -> Dict:
        """
        Extract topics from texts
        
        Args:
            texts: List of text strings
            num_topics: Number of topics to extract
            
        Returns:
            Dictionary with topics and their information
        """
        if not BERTOPIC_AVAILABLE or self.model is None:
            logger.warning("BERTopic not available")
            return {}
        
        try:
            # Filter out empty texts
            filtered_texts = [t for t in texts if t and len(str(t).strip()) > 0]
            
            if len(filtered_texts) < 5:
                logger.warning(f"Not enough texts for topic modeling ({len(filtered_texts)})")
                return {}
            
            # Fit the model
            topics, probabilities = self.model.fit_transform(filtered_texts)
            
            result = {
                "topics": {},
                "probabilities": probabilities.tolist() if isinstance(probabilities, np.ndarray) else probabilities
            }
            
            # Get topic information
            topic_info = self.model.get_topic_info()
            
            for idx, row in topic_info.iterrows():
                topic_id = int(row['Topic'])
                if topic_id >= 0:  # Skip outlier topic (-1)
                    result["topics"][str(topic_id)] = {
                        "name": row.get('Name', f'Topic {topic_id}'),
                        "count": int(row.get('Count', 0)),
                        "words": row.get('Representation', [])
                    }
            
            return result
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            return {}
    
    def add_topics_to_dataframe(self, df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
        """
        Add topic analysis to DataFrame
        
        Args:
            df: Input DataFrame
            text_column: Name of column containing text
            
        Returns:
            DataFrame with added topic column
        """
        if not BERTOPIC_AVAILABLE or self.model is None:
            logger.warning("BERTopic not available")
            return df
        
        try:
            df = df.copy()
            texts = df[text_column].fillna("").tolist()
            
            # Filter out empty texts
            filtered_texts = [t for t in texts if t and len(str(t).strip()) > 0]
            
            if len(filtered_texts) < 5:
                df["topic"] = -1
                return df
            
            topics, _ = self.model.fit_transform(filtered_texts)
            df["topic"] = topics
            
            return df
        except Exception as e:
            logger.error(f"Error adding topics to DataFrame: {e}")
            return df
    
    def get_topic_summary(self, df: pd.DataFrame) -> List[Dict]:
        """
        Get topic summary from DataFrame
        
        Args:
            df: DataFrame with topic column
            
        Returns:
            List of topic summary dictionaries
        """
        try:
            if "topic" not in df.columns:
                return []
            
            topic_dist = df["topic"].value_counts()
            total = len(df)
            
            result = []
            for topic, count in topic_dist.items():
                if topic >= 0:  # Skip outlier topic
                    result.append({
                        "topic_id": int(topic),
                        "count": int(count),
                        "percentage": round((count / total) * 100, 2)
                    })
            
            return sorted(result, key=lambda x: x["count"], reverse=True)
        except Exception as e:
            logger.error(f"Error getting topic summary: {e}")
            return []
    
    def get_top_documents_per_topic(self, df: pd.DataFrame, topic_id: int, limit: int = 5) -> List[str]:
        """
        Get top documents for a specific topic
        
        Args:
            df: DataFrame with topic column
            topic_id: Topic ID
            limit: Number of documents to return
            
        Returns:
            List of top documents (text strings)
        """
        try:
            if "topic" not in df.columns:
                return []
            
            topic_docs = df[df["topic"] == topic_id]
            
            # If text column exists, return top documents
            if "text" in topic_docs.columns:
                return topic_docs["text"].head(limit).tolist()
            
            return []
        except Exception as e:
            logger.error(f"Error getting top documents per topic: {e}")
            return []
    
    def get_fallback_topics(self, df: pd.DataFrame, text_column: str = "text", num_topics: int = 5) -> Dict:
        """
        Fallback method for topic extraction using simple clustering
        
        Args:
            df: Input DataFrame
            text_column: Name of column containing text
            num_topics: Number of topics
            
        Returns:
            Dictionary with topic information
        """
        try:
            # Simple approach: group by keyword frequency and sentiment
            texts = df[text_column].tolist()
            
            if "sentiment" in df.columns:
                sentiments = df["sentiment"].unique()
                return {
                    "topics": {str(i): {"name": sent, "count": len(df[df["sentiment"] == sent])} for i, sent in enumerate(sentiments)}
                }
            
            return {}
        except Exception as e:
            logger.error(f"Error in fallback topic extraction: {e}")
            return {}
