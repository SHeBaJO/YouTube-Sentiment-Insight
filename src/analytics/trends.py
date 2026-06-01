"""
Trend analysis for sentiment over time
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class TrendAnalyzer:
    """Analyze trends in sentiment and engagement over time"""
    
    @staticmethod
    def daily_sentiment_trends(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate daily sentiment trends
        
        Args:
            df: DataFrame with 'published_at' and 'sentiment' columns
            
        Returns:
            DataFrame with daily sentiment breakdown
        """
        df = df.copy()
        df["date"] = pd.to_datetime(df["published_at"]).dt.date
        
        daily_trends = df.groupby(["date", "sentiment"]).size().unstack(fill_value=0)
        
        return daily_trends
    
    @staticmethod
    def weekly_sentiment_trends(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate weekly sentiment trends
        
        Args:
            df: DataFrame with 'published_at' and 'sentiment' columns
            
        Returns:
            DataFrame with weekly sentiment breakdown
        """
        df = df.copy()
        df["published_at"] = pd.to_datetime(df["published_at"])
        df["week"] = df["published_at"].dt.isocalendar().week
        df["year"] = df["published_at"].dt.year
        
        weekly_trends = df.groupby(["year", "week", "sentiment"]).size().unstack(fill_value=0)
        
        return weekly_trends
    
    @staticmethod
    def sentiment_trend_over_time(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate sentiment proportions over time
        
        Args:
            df: DataFrame with 'published_at' and 'sentiment' columns
            
        Returns:
            DataFrame with sentiment proportions by date
        """
        daily = TrendAnalyzer.daily_sentiment_trends(df)
        
        # Calculate proportions
        proportions = daily.div(daily.sum(axis=1), axis=0) * 100
        
        return proportions
    
    @staticmethod
    def engagement_trend_analysis(df: pd.DataFrame, date_col: str = "published_at", likes_col: str = "likes") -> pd.DataFrame:
        """
        Analyze engagement trends over time
        
        Args:
            df: DataFrame with engagement metrics
            date_col: Date column name
            likes_col: Likes column name
            
        Returns:
            DataFrame with daily engagement metrics
        """
        df = df.copy()
        df["date"] = pd.to_datetime(df[date_col]).dt.date
        
        engagement_trends = df.groupby("date").agg({
            likes_col: ["mean", "sum", "max"],
            "sentiment": "count"
        }).rename(columns={"sentiment": "comment_count"})
        
        return engagement_trends
    
    @staticmethod
    def sentiment_correlation_with_likes(df: pd.DataFrame) -> Dict:
        """
        Calculate correlation between sentiment and likes
        
        Args:
            df: DataFrame with 'sentiment', 'confidence', and 'likes' columns
            
        Returns:
            Dictionary with correlation statistics
        """
        df = df.copy()
        
        # Convert sentiment to numeric
        sentiment_map = {"Positive 😊": 1, "Neutral 😐": 0, "Negative 😠": -1}
        df["sentiment_numeric"] = df["sentiment"].map(sentiment_map)
        
        # Calculate correlation
        correlation = df["sentiment_numeric"].corr(df["likes"])
        
        # Group by sentiment and calculate average likes
        avg_likes_by_sentiment = df.groupby("sentiment")["likes"].agg(["mean", "median", "std", "count"])
        
        return {
            "correlation": correlation,
            "avg_likes_by_sentiment": avg_likes_by_sentiment.to_dict(orient="index")
        }
    
    @staticmethod
    def hourly_sentiment_trends(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate hourly sentiment trends
        
        Args:
            df: DataFrame with 'published_at' and 'sentiment' columns
            
        Returns:
            DataFrame with hourly sentiment breakdown
        """
        df = df.copy()
        df["published_at"] = pd.to_datetime(df["published_at"])
        df["hour"] = df["published_at"].dt.hour
        
        hourly_trends = df.groupby(["hour", "sentiment"]).size().unstack(fill_value=0)
        
        return hourly_trends
    
    @staticmethod
    def get_trend_summary(df: pd.DataFrame) -> Dict:
        """
        Get summary statistics of trends
        
        Args:
            df: DataFrame with sentiment data
            
        Returns:
            Dictionary with trend summary
        """
        df = df.copy()
        df["published_at"] = pd.to_datetime(df["published_at"])
        
        # Time range
        time_span = (df["published_at"].max() - df["published_at"].min()).days
        
        # Sentiment trends
        first_half = df.iloc[:len(df)//2]
        second_half = df.iloc[len(df)//2:]
        
        first_positive = len(first_half[first_half["sentiment"].str.contains("Positive", na=False)]) / len(first_half) if len(first_half) > 0 else 0
        second_positive = len(second_half[second_half["sentiment"].str.contains("Positive", na=False)]) / len(second_half) if len(second_half) > 0 else 0
        
        sentiment_trend = "increasing" if second_positive > first_positive else "decreasing"
        
        return {
            "time_span_days": time_span,
            "sentiment_trend": sentiment_trend,
            "first_half_positive_pct": first_positive * 100,
            "second_half_positive_pct": second_positive * 100,
            "trend_change_pct": (second_positive - first_positive) * 100
        }
