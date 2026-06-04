"""
Analytics service for aggregated statistics and insights
"""
import pandas as pd
from typing import Dict, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for comprehensive analytics"""
    
    @staticmethod
    def get_engagement_metrics(df: pd.DataFrame) -> Dict:
        """
        Get engagement metrics from comments
        
        Args:
            df: DataFrame with comments
            
        Returns:
            Dictionary with engagement metrics
        """
        try:
            if df.empty or "likes" not in df.columns:
                return {}
            
            metrics = {
                "total_comments": len(df),
                "total_likes": int(df["likes"].sum()),
                "average_likes": round(df["likes"].mean(), 2),
                "max_likes": int(df["likes"].max()),
                "engagement_rate": round((df["likes"].sum() / len(df)) if len(df) > 0 else 0, 2)
            }
            
            if "reply_count" in df.columns:
                metrics["total_replies"] = int(df["reply_count"].sum())
                metrics["average_replies"] = round(df["reply_count"].mean(), 2)
            
            return metrics
        except Exception as e:
            logger.error(f"Error getting engagement metrics: {e}")
            return {}
    
    @staticmethod
    def get_sentiment_vs_likes(df: pd.DataFrame) -> Dict:
        """
        Correlate sentiment with likes
        
        Args:
            df: DataFrame with sentiment and likes
            
        Returns:
            Dictionary with sentiment-likes correlation
        """
        try:
            if df.empty or "sentiment" not in df.columns or "likes" not in df.columns:
                return {}
            
            result = {}
            for sentiment in df["sentiment"].unique():
                sentiment_df = df[df["sentiment"] == sentiment]
                result[sentiment] = {
                    "count": len(sentiment_df),
                    "average_likes": round(sentiment_df["likes"].mean(), 2),
                    "total_likes": int(sentiment_df["likes"].sum())
                }
            
            return result
        except Exception as e:
            logger.error(f"Error getting sentiment vs likes: {e}")
            return {}
    
    @staticmethod
    def get_trending_topics(df: pd.DataFrame, limit: int = 10) -> List[Dict]:
        """
        Get trending topics
        
        Args:
            df: DataFrame with keywords
            limit: Number of topics to return
            
        Returns:
            List of trending topics
        """
        try:
            if df.empty or "keywords" not in df.columns:
                return []
            
            from collections import Counter
            
            all_keywords = []
            for keywords_list in df["keywords"]:
                if isinstance(keywords_list, list):
                    all_keywords.extend(keywords_list)
            
            keyword_freq = Counter(all_keywords)
            top_keywords = keyword_freq.most_common(limit)
            
            result = []
            for keyword, count in top_keywords:
                result.append({
                    "topic": keyword,
                    "count": int(count),
                    "trend": "increasing"  # Simplified
                })
            
            return result
        except Exception as e:
            logger.error(f"Error getting trending topics: {e}")
            return []
    
    @staticmethod
    def get_channel_analytics(video_info: Dict, df: pd.DataFrame) -> Dict:
        """
        Get comprehensive channel analytics
        
        Args:
            video_info: Video information dictionary
            df: Comments DataFrame
            
        Returns:
            Dictionary with channel analytics
        """
        try:
            analytics = {
                "video_title": video_info.get("title", ""),
                "channel_name": video_info.get("channel_name", ""),
                "video_views": video_info.get("view_count", 0),
                "video_likes": video_info.get("like_count", 0),
                "total_comments_analyzed": len(df),
                "video_comment_count": video_info.get("comment_count", 0),
                "published_at": video_info.get("published_at", "")
            }
            
            if not df.empty:
                # Add sentiment analysis
                if "sentiment" in df.columns:
                    sentiment_counts = df["sentiment"].value_counts()
                    analytics["sentiment_breakdown"] = {
                        "positive": int(sentiment_counts.get("Positive", 0)),
                        "negative": int(sentiment_counts.get("Negative", 0)),
                        "neutral": int(sentiment_counts.get("Neutral", 0))
                    }
                
                # Add engagement metrics
                if "likes" in df.columns:
                    analytics["engagement"] = {
                        "total_likes": int(df["likes"].sum()),
                        "average_likes_per_comment": round(df["likes"].mean(), 2)
                    }
            
            return analytics
        except Exception as e:
            logger.error(f"Error getting channel analytics: {e}")
            return {}
    
    @staticmethod
    def get_sentiment_trends(df: pd.DataFrame) -> List[Dict]:
        """
        Get sentiment trends over time
        
        Args:
            df: DataFrame with sentiment and published_at
            
        Returns:
            List of sentiment trends
        """
        try:
            if df.empty or "published_at" not in df.columns or "sentiment" not in df.columns:
                return []
            
            df = df.copy()
            df["published_at"] = pd.to_datetime(df["published_at"])
            df["date"] = df["published_at"].dt.date
            
            daily_sentiment = df.groupby(["date", "sentiment"]).size().unstack(fill_value=0)
            
            result = []
            for date in daily_sentiment.index:
                result.append({
                    "date": str(date),
                    "positive": int(daily_sentiment.loc[date, "Positive"] if "Positive" in daily_sentiment.columns else 0),
                    "negative": int(daily_sentiment.loc[date, "Negative"] if "Negative" in daily_sentiment.columns else 0),
                    "neutral": int(daily_sentiment.loc[date, "Neutral"] if "Neutral" in daily_sentiment.columns else 0)
                })
            
            return result
        except Exception as e:
            logger.error(f"Error getting sentiment trends: {e}")
            return []
