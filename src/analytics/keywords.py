"""
Keyword extraction and analysis
"""
import pandas as pd
from typing import List, Dict, Tuple
from collections import Counter
import re
import logging

logger = logging.getLogger(__name__)


class KeywordExtractor:
    """Extract keywords from text"""
    
    # Common stopwords
    STOPWORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "must", "can", "this", "that",
        "these", "those", "i", "you", "he", "she", "it", "we", "they", "me",
        "him", "her", "us", "them", "what", "which", "who", "whom", "where",
        "when", "why", "how", "all", "each", "every", "both", "few", "more",
        "most", "other", "some", "such", "any", "no", "nor", "not", "only",
        "same", "so", "than", "too", "very", "just", "as", "if", "because",
        "while", "although", "though", "since", "before", "after", "above",
        "below", "under", "over", "between", "through", "during", "about",
        "am", "pm", "youtube", "video", "channel", "like", "lol", "haha",
        "yeah", "okay", "ok", "yep", "nope", "sure", "got", "got", "nice",
        "good", "bad", "thing", "things", "way", "said", "say", "says"
    }
    
    def __init__(self, min_length: int = 3):
        """
        Initialize keyword extractor
        
        Args:
            min_length: Minimum word length for keywords
        """
        self.min_length = min_length
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r"http\S+|www\S+", "", text)
        
        # Remove email addresses
        text = re.sub(r"\S+@\S+", "", text)
        
        # Remove special characters but keep spaces
        text = re.sub(r"[^\w\s]", " ", text)
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            
        Returns:
            List of keywords
        """
        cleaned = self.clean_text(text)
        words = cleaned.split()
        
        keywords = [
            word for word in words
            if len(word) >= self.min_length
            and word not in self.STOPWORDS
        ]
        
        return keywords
    
    def extract_batch_keywords(self, texts: List[str]) -> List[List[str]]:
        """
        Extract keywords from multiple texts
        
        Args:
            texts: List of texts
            
        Returns:
            List of keyword lists
        """
        return [self.extract_keywords(text) for text in texts]
    
    def get_top_keywords(
        self,
        texts: List[str],
        top_n: int = 10
    ) -> List[Tuple[str, int]]:
        """
        Get most frequent keywords from texts
        
        Args:
            texts: List of texts
            top_n: Number of top keywords to return
            
        Returns:
            List of (keyword, frequency) tuples
        """
        all_keywords = []
        
        for text in texts:
            keywords = self.extract_keywords(text)
            all_keywords.extend(keywords)
        
        keyword_counts = Counter(all_keywords)
        
        return keyword_counts.most_common(top_n)


def analyze_keywords(df: pd.DataFrame, text_column: str = "text", top_n: int = 10) -> Dict:
    """
    Analyze keywords in DataFrame
    
    Args:
        df: Input DataFrame
        text_column: Column containing text
        top_n: Number of top keywords
        
    Returns:
        Dictionary with keyword analysis
    """
    extractor = KeywordExtractor()
    
    top_keywords = extractor.get_top_keywords(
        df[text_column].astype(str).tolist(),
        top_n=top_n
    )
    
    return {
        "top_keywords": top_keywords,
        "total_unique": len(set(kw for text in df[text_column] for kw in extractor.extract_keywords(text))),
        "keyword_pairs": [(kw, count) for kw, count in top_keywords]
    }


def get_keyword_frequency_distribution(
    df: pd.DataFrame,
    text_column: str = "text",
    top_n: int = 20
) -> pd.DataFrame:
    """
    Get keyword frequency distribution as DataFrame
    
    Args:
        df: Input DataFrame
        text_column: Column containing text
        top_n: Number of top keywords
        
    Returns:
        DataFrame with keyword frequencies
    """
    extractor = KeywordExtractor()
    
    top_keywords = extractor.get_top_keywords(
        df[text_column].astype(str).tolist(),
        top_n=top_n
    )
    
    keywords_df = pd.DataFrame(
        top_keywords,
        columns=["Keyword", "Frequency"]
    )
    
    return keywords_df
