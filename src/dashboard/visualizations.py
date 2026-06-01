"""
Visualization utilities for the dashboard
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class DashboardVisualizations:
    """Create dashboard visualizations"""
    
    @staticmethod
    def sentiment_pie_chart(sentiment_counts: Dict) -> go.Figure:
        """
        Create sentiment distribution pie chart
        
        Args:
            sentiment_counts: Dictionary with sentiment counts
            
        Returns:
            Plotly figure
        """
        labels = list(sentiment_counts.keys())
        values = list(sentiment_counts.values())
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                marker=dict(
                    colors=["#FF6B6B", "#4ECDC4", "#95A5A6"]
                )
            )
        ])
        
        fig.update_layout(
            title="Sentiment Distribution",
            height=400
        )
        
        return fig
    
    @staticmethod
    def sentiment_bar_chart(sentiment_df: pd.DataFrame) -> go.Figure:
        """
        Create sentiment bar chart
        
        Args:
            sentiment_df: DataFrame with sentiment data
            
        Returns:
            Plotly figure
        """
        fig = px.bar(
            sentiment_df,
            x="Sentiment",
            y="Count",
            color="Sentiment",
            color_discrete_map={
                "Positive 😊": "#FF6B6B",
                "Negative 😠": "#4ECDC4",
                "Neutral 😐": "#95A5A6"
            },
            title="Sentiment Count Distribution",
            height=400
        )
        
        fig.update_layout(
            xaxis_title="Sentiment",
            yaxis_title="Count"
        )
        
        return fig
    
    @staticmethod
    def wordcloud(texts: List[str]) -> plt.Figure:
        """
        Create word cloud
        
        Args:
            texts: List of texts
            
        Returns:
            Matplotlib figure
        """
        text = " ".join(texts)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color="white",
            colormap="viridis"
        ).generate(text)
        
        ax.imshow(wordcloud)
        ax.axis("off")
        
        return fig
    
    @staticmethod
    def sentiment_trend_chart(trend_df: pd.DataFrame) -> go.Figure:
        """
        Create sentiment trend line chart
        
        Args:
            trend_df: DataFrame with trend data
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        for sentiment in trend_df.columns:
            fig.add_trace(go.Scatter(
                x=trend_df.index,
                y=trend_df[sentiment],
                mode="lines+markers",
                name=sentiment
            ))
        
        fig.update_layout(
            title="Sentiment Trends Over Time",
            xaxis_title="Date",
            yaxis_title="Count",
            hovermode="x unified",
            height=400
        )
        
        return fig
    
    @staticmethod
    def keyword_bar_chart(keywords_df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Create keyword frequency bar chart
        
        Args:
            keywords_df: DataFrame with keywords
            top_n: Number of top keywords
            
        Returns:
            Plotly figure
        """
        top_keywords = keywords_df.head(top_n)
        
        fig = px.bar(
            top_keywords,
            x="Frequency",
            y="Keyword",
            orientation="h",
            title=f"Top {top_n} Keywords",
            height=400
        )
        
        fig.update_layout(
            yaxis_title="Keyword",
            xaxis_title="Frequency"
        )
        
        return fig
    
    @staticmethod
    def emotion_distribution_chart(emotion_stats: Dict) -> go.Figure:
        """
        Create emotion distribution chart
        
        Args:
            emotion_stats: Dictionary with emotion statistics
            
        Returns:
            Plotly figure
        """
        emotions = list(emotion_stats.keys())
        counts = [emotion_stats[e]["count"] for e in emotions]
        
        fig = px.bar(
            x=emotions,
            y=counts,
            title="Emotion Distribution",
            labels={"x": "Emotion", "y": "Count"},
            height=400
        )
        
        return fig
    
    @staticmethod
    def likes_distribution_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create likes distribution chart
        
        Args:
            df: DataFrame with likes data
            
        Returns:
            Plotly figure
        """
        fig = px.histogram(
            df,
            x="likes",
            nbins=30,
            title="Like Count Distribution",
            labels={"likes": "Number of Likes"},
            height=400
        )
        
        return fig
    
    @staticmethod
    def sentiment_vs_likes_scatter(df: pd.DataFrame) -> go.Figure:
        """
        Create scatter plot of sentiment vs likes
        
        Args:
            df: DataFrame with sentiment and likes
            
        Returns:
            Plotly figure
        """
        sentiment_map = {
            "Positive 😊": 1,
            "Neutral 😐": 0,
            "Negative 😠": -1
        }
        
        df = df.copy()
        df["sentiment_numeric"] = df["sentiment"].map(sentiment_map)
        
        fig = px.scatter(
            df,
            x="sentiment_numeric",
            y="likes",
            color="sentiment",
            title="Sentiment vs. Likes",
            labels={"sentiment_numeric": "Sentiment", "likes": "Likes"},
            height=400
        )
        
        return fig
    
    @staticmethod
    def topic_distribution_chart(topics_df: pd.DataFrame) -> go.Figure:
        """
        Create topic distribution chart
        
        Args:
            topics_df: DataFrame with topic data
            
        Returns:
            Plotly figure
        """
        fig = px.pie(
            topics_df,
            values="Count",
            names="Topic",
            title="Topic Distribution",
            height=400
        )
        
        return fig
