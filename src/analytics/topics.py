"""
Topic modeling using BERTopic
"""
import streamlit as st
import pandas as pd
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

# BERTopic will be installed via requirements.txt
try:
    from bertopic import BERTopic
    BERTOPIC_AVAILABLE = True
except ImportError:
    BERTOPIC_AVAILABLE = False


class TopicModeler:
    """Perform topic modeling on comments"""
    
    def __init__(self, min_topic_size: int = 5, nr_topics: str = "auto"):
        """
        Initialize topic modeler
        
        Args:
            min_topic_size: Minimum topic size
            nr_topics: Number of topics ('auto' for automatic)
        """
        if not BERTOPIC_AVAILABLE:
            raise ImportError("BERTopic not installed. Install with: pip install bertopic")
        
        self.min_topic_size = min_topic_size
        self.nr_topics = nr_topics
        self._model = None
    
    @property
    def model(self):
        """Lazy load BERTopic model"""
        if self._model is None:
            with st.spinner("Loading topic modeling model..."):
                self._model = BERTopic(
                    min_topic_size=self.min_topic_size,
                    nr_topics=self.nr_topics,
                    language="english"
                )
        return self._model
    
    def fit_topics(self, texts: List[str]) -> Tuple[List[int], List[Dict]]:
        """
        Fit topics to documents
        
        Args:
            texts: List of document texts
            
        Returns:
            Tuple of (topic assignments, topic info)
        """
        try:
            topics, probs = self.model.fit_transform(texts)
            
            # Get topic information
            topic_info = self.model.get_topic_info()
            
            return topics, topic_info.to_dict(orient="records")
        except Exception as e:
            logger.error(f"Error fitting topics: {e}")
            return [], []
    
    def get_topics(self) -> Dict:
        """
        Get all topics with keywords
        
        Returns:
            Dictionary mapping topic IDs to keywords
        """
        try:
            topics = self.model.get_topics()
            return {
                topic_id: [word for word, score in words]
                for topic_id, words in topics.items()
            }
        except Exception as e:
            logger.error(f"Error getting topics: {e}")
            return {}
    
    def get_topic_distribution(self, topics: List[int]) -> Dict:
        """
        Get distribution of topics
        
        Args:
            topics: List of topic assignments
            
        Returns:
            Dictionary with topic frequencies
        """
        from collections import Counter
        
        topic_counts = Counter(topics)
        total = len(topics)
        
        return {
            "topic_id": list(topic_counts.keys()),
            "count": list(topic_counts.values()),
            "percentage": [count / total * 100 for count in topic_counts.values()]
        }


def add_topics_to_dataframe(
    df: pd.DataFrame,
    texts: List[str],
    min_topic_size: int = 5
) -> pd.DataFrame:
    """
    Add topic assignments to DataFrame
    
    Args:
        df: Input DataFrame
        texts: List of texts
        min_topic_size: Minimum topic size
        
    Returns:
        DataFrame with topic column
    """
    if not BERTOPIC_AVAILABLE:
        st.warning("BERTopic not installed. Topic modeling unavailable.")
        return df
    
    try:
        modeler = TopicModeler(min_topic_size=min_topic_size)
        topics, _ = modeler.fit_topics(texts)
        
        df = df.copy()
        df["topic"] = topics
        
        return df
    except Exception as e:
        logger.error(f"Error adding topics: {e}")
        st.warning(f"Topic modeling error: {e}")
        return df


def get_topic_summary(df: pd.DataFrame, topic_col: str = "topic") -> pd.DataFrame:
    """
    Get summary of topics
    
    Args:
        df: DataFrame with topic column
        topic_col: Name of topic column
        
    Returns:
        DataFrame with topic frequencies
    """
    if topic_col not in df.columns:
        return pd.DataFrame()
    
    topic_counts = df[topic_col].value_counts().reset_index()
    topic_counts.columns = ["Topic", "Count"]
    topic_counts["Percentage"] = (topic_counts["Count"] / len(df) * 100).round(2)
    
    return topic_counts
