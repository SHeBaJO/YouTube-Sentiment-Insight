"""
Export utilities for reports and data
"""
import pandas as pd
from typing import Dict
import io
import logging

logger = logging.getLogger(__name__)


class ReportExporter:
    """Export analysis results to various formats"""
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: str = "sentiment_analysis.csv") -> bytes:
        """
        Export DataFrame to CSV
        
        Args:
            df: Input DataFrame
            filename: Output filename
            
        Returns:
            CSV bytes
        """
        return df.to_csv(index=False).encode()
    
    @staticmethod
    def export_to_excel(
        df: pd.DataFrame,
        filename: str = "sentiment_analysis.xlsx",
        sheet_name: str = "Comments"
    ) -> bytes:
        """
        Export DataFrame to Excel
        
        Args:
            df: Input DataFrame
            filename: Output filename
            sheet_name: Sheet name in Excel
            
        Returns:
            Excel bytes
        """
        try:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            return output.getvalue()
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            raise
    
    @staticmethod
    def create_sentiment_report(
        df: pd.DataFrame,
        video_info: Dict
    ) -> pd.DataFrame:
        """
        Create comprehensive sentiment report
        
        Args:
            df: Comments DataFrame
            video_info: Video metadata
            
        Returns:
            Report DataFrame
        """
        report_data = {
            "Metric": [
                "Video Title",
                "Channel",
                "Total Comments",
                "Positive Comments",
                "Negative Comments",
                "Neutral Comments",
                "Positive %",
                "Negative %",
                "Neutral %",
                "Average Confidence",
                "Average Likes per Comment",
                "Total Engagement",
                "Most Common Sentiment"
            ],
            "Value": [
                video_info.get("title", "N/A"),
                video_info.get("channel_title", "N/A"),
                len(df),
                len(df[df["sentiment"].str.contains("Positive", na=False)]),
                len(df[df["sentiment"].str.contains("Negative", na=False)]),
                len(df[df["sentiment"].str.contains("Neutral", na=False)]),
                f"{len(df[df['sentiment'].str.contains('Positive', na=False)]) / len(df) * 100:.2f}%",
                f"{len(df[df['sentiment'].str.contains('Negative', na=False)]) / len(df) * 100:.2f}%",
                f"{len(df[df['sentiment'].str.contains('Neutral', na=False)]) / len(df) * 100:.2f}%",
                f"{df['confidence'].mean():.2f}",
                f"{df['likes'].mean():.2f}",
                int(df['likes'].sum()),
                df["sentiment"].mode()[0] if len(df) > 0 else "N/A"
            ]
        }
        
        return pd.DataFrame(report_data)
    
    @staticmethod
    def create_emotion_report(
        df: pd.DataFrame,
        emotion_stats: Dict
    ) -> pd.DataFrame:
        """
        Create emotion analysis report
        
        Args:
            df: Comments DataFrame with emotions
            emotion_stats: Emotion statistics
            
        Returns:
            Report DataFrame
        """
        report_data = {
            "Emotion": [],
            "Count": [],
            "Percentage": [],
            "Average Confidence": []
        }
        
        for emotion, stats in emotion_stats.get("emotion_distribution", {}).items():
            report_data["Emotion"].append(emotion.capitalize())
            report_data["Count"].append(stats["count"])
            report_data["Percentage"].append(f"{stats['percentage']:.2f}%")
            
            emotion_df = df[df["emotion"] == emotion]
            avg_conf = emotion_df["emotion_confidence"].mean() if len(emotion_df) > 0 else 0
            report_data["Average Confidence"].append(f"{avg_conf:.2f}")
        
        return pd.DataFrame(report_data)
    
    @staticmethod
    def create_engagement_report(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create engagement metrics report
        
        Args:
            df: Comments DataFrame with likes
            
        Returns:
            Report DataFrame
        """
        report_data = {
            "Metric": [
                "Total Comments",
                "Total Likes",
                "Average Likes per Comment",
                "Median Likes",
                "Max Likes",
                "Min Likes",
                "Std Dev Likes",
                "Comments with 0 Likes",
                "Most Liked Comment Likes"
            ],
            "Value": [
                len(df),
                int(df["likes"].sum()),
                f"{df['likes'].mean():.2f}",
                int(df["likes"].median()),
                int(df["likes"].max()),
                int(df["likes"].min()),
                f"{df['likes'].std():.2f}",
                len(df[df["likes"] == 0]),
                int(df["likes"].max())
            ]
        }
        
        return pd.DataFrame(report_data)
    
    @staticmethod
    def create_keyword_report(keywords_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create keyword analysis report
        
        Args:
            keywords_df: Keywords DataFrame
            
        Returns:
            Report DataFrame
        """
        keywords_df = keywords_df.copy()
        keywords_df["Percentage"] = (
            keywords_df["Frequency"] / keywords_df["Frequency"].sum() * 100
        ).round(2)
        
        return keywords_df
    
    @staticmethod
    def export_multisheet_excel(
        dataframes: Dict[str, pd.DataFrame],
        filename: str = "sentiment_analysis_report.xlsx"
    ) -> bytes:
        """
        Export multiple DataFrames to Excel with multiple sheets
        
        Args:
            dataframes: Dictionary mapping sheet names to DataFrames
            filename: Output filename
            
        Returns:
            Excel bytes
        """
        try:
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                for sheet_name, df in dataframes.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            return output.getvalue()
        except Exception as e:
            logger.error(f"Error exporting multi-sheet Excel: {e}")
            raise
