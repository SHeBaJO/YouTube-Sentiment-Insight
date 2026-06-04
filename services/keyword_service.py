"""
Keyword extraction and analysis service
"""
import pandas as pd
from typing import List, Dict
import re
import logging
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

logger = logging.getLogger(__name__)


class KeywordService:
    """Service for keyword extraction and analysis"""
    
    def __init__(self):
        """Initialize keyword service"""
        self.stop_words = set(stopwords.words('english'))
    
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
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove mentions and hashtags symbols but keep the text
        text = re.sub(r'@\w+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            min_length: Minimum keyword length
            
        Returns:
            List of keywords
        """
        try:
            cleaned_text = self.clean_text(text)
            tokens = word_tokenize(cleaned_text)
            
            keywords = [
                word for word in tokens
                if len(word) >= min_length and word not in self.stop_words
            ]
            
            return keywords
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def analyze_keywords(self, texts: List[str], top_k: int = 20) -> Dict[str, int]:
        """
        Analyze keywords from multiple texts
        
        Args:
            texts: List of text strings
            top_k: Number of top keywords to return
            
        Returns:
            Dictionary with keywords and their frequencies
        """
        try:
            all_keywords = []
            
            for text in texts:
                keywords = self.extract_keywords(text)
                all_keywords.extend(keywords)
            
            keyword_freq = Counter(all_keywords)
            top_keywords = dict(keyword_freq.most_common(top_k))
            
            return top_keywords
        except Exception as e:
            logger.error(f"Error analyzing keywords: {e}")
            return {}
    
    def add_keywords_to_dataframe(self, df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
        """
        Add extracted keywords to DataFrame
        
        Args:
            df: Input DataFrame
            text_column: Name of column containing text
            
        Returns:
            DataFrame with added keywords column
        """
        try:
            df = df.copy()
            df["keywords"] = df[text_column].apply(lambda x: self.extract_keywords(x))
            return df
        except Exception as e:
            logger.error(f"Error adding keywords to DataFrame: {e}")
            return df
    
    def get_keyword_frequency(self, df: pd.DataFrame, top_k: int = 20) -> List[Dict]:
        """
        Get keyword frequency from DataFrame
        
        Args:
            df: DataFrame with keywords column
            top_k: Number of top keywords to return
            
        Returns:
            List of keyword frequency dictionaries
        """
        try:
            if "keywords" not in df.columns:
                return []
            
            all_keywords = []
            for keywords_list in df["keywords"]:
                if isinstance(keywords_list, list):
                    all_keywords.extend(keywords_list)
            
            keyword_freq = Counter(all_keywords)
            top_keywords = keyword_freq.most_common(top_k)
            
            result = []
            for keyword, freq in top_keywords:
                result.append({
                    "keyword": keyword,
                    "frequency": int(freq),
                    "percentage": round((freq / len(all_keywords)) * 100, 2) if all_keywords else 0
                })
            
            return result
        except Exception as e:
            logger.error(f"Error getting keyword frequency: {e}")
            return []
    
    def filter_by_keyword(self, df: pd.DataFrame, keyword: str) -> pd.DataFrame:
        """
        Filter DataFrame by keyword
        
        Args:
            df: Input DataFrame
            keyword: Keyword to filter by
            
        Returns:
            Filtered DataFrame
        """
        try:
            if "keywords" not in df.columns:
                return pd.DataFrame()
            
            mask = df["keywords"].apply(lambda x: keyword.lower() in [k.lower() for k in (x if isinstance(x, list) else [])])
            return df[mask]
        except Exception as e:
            logger.error(f"Error filtering by keyword: {e}")
            return pd.DataFrame()
