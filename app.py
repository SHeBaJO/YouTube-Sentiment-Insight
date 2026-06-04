"""
YouTube Comment Sentiment Analysis Dashboard
Main Streamlit application
"""
import streamlit as st
import pandas as pd
import logging
from datetime import datetime

# Import from src modules
from src.config import config
from src.utils.youtube_api import YouTubeCommentExtractor, create_comments_dataframe
from src.models.sentiment import SentimentAnalyzer, add_sentiment_to_dataframe, get_sentiment_statistics
from src.models.emotion import EmotionDetector, add_emotion_to_dataframe, get_emotion_statistics
from src.analytics.keywords import KeywordExtractor, analyze_keywords, get_keyword_frequency_distribution
from src.analytics.trends import TrendAnalyzer
from src.analytics.topics import add_topics_to_dataframe, get_topic_summary
from src.dashboard.visualizations import DashboardVisualizations
from src.dashboard.export import ReportExporter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="YouTube Sentiment Analysis Dashboard",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    
    .stButton > button {
        background-color: #FF0000;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    
    .metric-card {
        background-color: #1c1c1c;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #FF0000;
    }
    
    h1, h2, h3 {
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# TITLE AND DESCRIPTION
# ============================================================================
st.title("🎥 YouTube Comment Sentiment Analysis Dashboard")

st.markdown("""
Analyze YouTube comments using advanced **NLP**, **Sentiment Analysis**, and **Machine Learning**.

This tool provides:
- 🧠 Transformer-based sentiment analysis
- 😊 Emotion detection and analysis
- 🔑 Keyword extraction and trends
- 📊 Interactive visualizations
- 💾 Export reports in multiple formats
""")

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================
st.sidebar.header("⚙️ Configuration")

# Check if API key is configured
if config is None:
    st.error("""
    ❌ YouTube API Key not found!
    
    Please set your API key using one of these methods:
    1. Create `.streamlit/secrets.toml` with: `YOUTUBE_API_KEY = "your_key"`
    2. Set environment variable: `export YOUTUBE_API_KEY="your_key"`
    
    Get your API key from: https://console.cloud.google.com/
    """)
    st.stop()

# Analysis parameters
max_comments = st.sidebar.slider(
    "📊 Maximum Comments to Analyze",
    min_value=10,
    max_value=500,
    value=100,
    step=10
)

# Feature toggles
st.sidebar.subheader("🔧 Features")
enable_emotion = st.sidebar.checkbox("Enable Emotion Detection", value=True)
enable_keywords = st.sidebar.checkbox("Enable Keyword Analysis", value=True)
enable_trends = st.sidebar.checkbox("Enable Trend Analysis", value=True)
enable_topics = st.sidebar.checkbox("Enable Topic Modeling", value=False)  # Disabled by default due to compute

# ============================================================================
# MAIN INPUT SECTION
# ============================================================================
st.markdown("---")
st.subheader("📹 YouTube Video Analysis")

# Input field
youtube_url = st.text_input(
    "Enter YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

# Analyze button
analyze_button = st.button("🚀 Analyze Comments", use_container_width=True)

# ============================================================================
# ANALYSIS EXECUTION
# ============================================================================
if analyze_button:
    if not youtube_url:
        st.error("❌ Please enter a YouTube video URL")
        st.stop()
    
    try:
        # Extract video ID
        extractor = YouTubeCommentExtractor(config.YOUTUBE_API_KEY)
        video_id = extractor.extract_video_id(youtube_url)
        
        if not video_id:
            st.error("❌ Invalid YouTube URL. Please check and try again.")
            st.stop()
        
        # Get video information
        with st.spinner("📹 Fetching video information..."):
            video_info = extractor.get_video_info(video_id)
            
            if not video_info:
                st.error("❌ Could not fetch video information. Video may be private or unavailable.")
                st.stop()
            
            st.success(f"✅ Video found: {video_info.get('title', 'Unknown')}")
        
        # Fetch comments
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("💬 Fetching YouTube comments..."):
            def progress_callback(progress):
                progress_bar.progress(progress)
                status_text.text(f"Fetched: {int(progress * max_comments)}/{max_comments} comments")
            
            comments_data = extractor.fetch_comments(
                video_id,
                max_comments=max_comments,
                progress_callback=progress_callback
            )
        
        if not comments_data:
            st.error("❌ No comments found for this video.")
            st.stop()
        
        # Create DataFrame
        df = create_comments_dataframe(comments_data)
        
        # Sentiment Analysis
        with st.spinner("🧠 Analyzing sentiment..."):
            sentiment_analyzer = SentimentAnalyzer()
            df = add_sentiment_to_dataframe(df, sentiment_analyzer, text_column="text")
        
        # Emotion Detection
        if enable_emotion:
            with st.spinner("😊 Detecting emotions..."):
                emotion_detector = EmotionDetector()
                df = add_emotion_to_dataframe(df, emotion_detector, text_column="text")
        
        # Keyword Extraction
        if enable_keywords:
            with st.spinner("🔑 Extracting keywords..."):
                keywords_analysis = analyze_keywords(df, text_column="text", top_n=20)
        
        # Topic Modeling
        if enable_topics:
            with st.spinner("📚 Performing topic modeling..."):
                df = add_topics_to_dataframe(df, df["text"].tolist())
        
        # ====================================================================
        # DASHBOARD DISPLAY
        # ====================================================================
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        # Get statistics
        sentiment_stats = get_sentiment_statistics(df)
        
        # KPI Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("📝 Total Comments", sentiment_stats["total_comments"])
        
        with col2:
            st.metric("😊 Positive", f"{sentiment_stats['positive']} ({sentiment_stats['positive_pct']:.1f}%)")
        
        with col3:
            st.metric("😠 Negative", f"{sentiment_stats['negative']} ({sentiment_stats['negative_pct']:.1f}%)")
        
        with col4:
            st.metric("😐 Neutral", f"{sentiment_stats['neutral']} ({sentiment_stats['neutral_pct']:.1f}%)")
        
        with col5:
            st.metric("⭐ Avg Confidence", f"{sentiment_stats['average_confidence']:.2f}")
        
        # Engagement metrics
        st.markdown("---")
        st.subheader("💬 Engagement Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👍 Total Likes", int(df["likes"].sum()))
        
        with col2:
            st.metric("📊 Average Likes", f"{df['likes'].mean():.1f}")
        
        with col3:
            st.metric("🔝 Max Likes", int(df["likes"].max()))
        
        with col4:
            st.metric("💬 Average Replies", f"{df.get('reply_count', pd.Series([0])).mean():.1f}")
        
        # ====================================================================
        # VISUALIZATIONS
        # ====================================================================
        st.markdown("---")
        st.subheader("📈 Visualizations")
        
        # Sentiment Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            sentiment_counts = df["sentiment"].value_counts().to_dict()
            fig_pie = DashboardVisualizations.sentiment_pie_chart(sentiment_counts)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            sentiment_df = pd.DataFrame({
                "Sentiment": sentiment_counts.keys(),
                "Count": sentiment_counts.values()
            })
            fig_bar = DashboardVisualizations.sentiment_bar_chart(sentiment_df)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Word Cloud
        st.subheader("☁️ Word Cloud")
        fig_wordcloud = DashboardVisualizations.wordcloud(df["text"].tolist())
        st.pyplot(fig_wordcloud, use_container_width=True)
        
        # Engagement Analysis
        st.subheader("💬 Engagement Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_likes = DashboardVisualizations.likes_distribution_chart(df)
            st.plotly_chart(fig_likes, use_container_width=True)
        
        with col2:
            fig_scatter = DashboardVisualizations.sentiment_vs_likes_scatter(df)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Keyword Analysis
        if enable_keywords:
            st.markdown("---")
            st.subheader("🔑 Keyword Analysis")
            
            keywords_df = get_keyword_frequency_distribution(df, text_column="text", top_n=15)
            fig_keywords = DashboardVisualizations.keyword_bar_chart(keywords_df, top_n=15)
            st.plotly_chart(fig_keywords, use_container_width=True)
            
            st.dataframe(keywords_df, use_container_width=True)
        
        # Emotion Analysis
        if enable_emotion:
            st.markdown("---")
            st.subheader("😊 Emotion Analysis")
            
            emotion_stats = get_emotion_statistics(df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Dominant Emotion:** {emotion_stats['dominant_emotion'].capitalize()} 🎯")
                st.write(f"**Average Confidence:** {emotion_stats['average_confidence']:.2f}")
            
            with col2:
                fig_emotion = DashboardVisualizations.emotion_distribution_chart(
                    emotion_stats["emotion_distribution"]
                )
                st.plotly_chart(fig_emotion, use_container_width=True)
        
        # Trend Analysis
        if enable_trends:
            st.markdown("---")
            st.subheader("📈 Sentiment Trends")
            
            daily_trends = TrendAnalyzer.daily_sentiment_trends(df)
            trend_summary = TrendAnalyzer.get_trend_summary(df)
            
            fig_trend = DashboardVisualizations.sentiment_trend_chart(daily_trends)
            st.plotly_chart(fig_trend, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Time Span:** {trend_summary['time_span_days']} days")
            
            with col2:
                st.write(f"**Trend:** {trend_summary['sentiment_trend'].upper()}")
            
            with col3:
                st.write(f"**Change:** {trend_summary['trend_change_pct']:.1f}%")
        
        # Topic Modeling
        if enable_topics and "topic" in df.columns:
            st.markdown("---")
            st.subheader("📚 Topic Analysis")
            
            topics_df = get_topic_summary(df)
            
            if not topics_df.empty:
                fig_topics = DashboardVisualizations.topic_distribution_chart(topics_df)
                st.plotly_chart(fig_topics, use_container_width=True)
                st.dataframe(topics_df, use_container_width=True)
        
        # ====================================================================
        # FILTERING AND DETAILED VIEW
        # ====================================================================
        st.markdown("---")
        st.subheader("🔍 Filter & Detailed View")
        
        filter_col1, filter_col2 = st.columns([2, 1])
        
        with filter_col1:
            filter_option = st.selectbox(
                "Filter by Sentiment",
                ["All", "Positive 😊", "Negative 😠", "Neutral 😐"]
            )
        
        with filter_col2:
            sort_by = st.selectbox(
                "Sort by",
                ["Likes (Descending)", "Date (Newest)", "Confidence"]
            )
        
        # Apply filters
        if filter_option == "All":
            filtered_df = df.copy()
        else:
            filtered_df = df[df["sentiment"] == filter_option].copy()
        
        # Apply sorting
        if sort_by == "Likes (Descending)":
            filtered_df = filtered_df.sort_values("likes", ascending=False)
        elif sort_by == "Date (Newest)":
            filtered_df = filtered_df.sort_values("published_at", ascending=False)
        elif sort_by == "Confidence":
            filtered_df = filtered_df.sort_values("confidence", ascending=False)
        
        # Display filtered data
        st.dataframe(filtered_df, use_container_width=True)
        
        # ====================================================================
        # EXPORT SECTION
        # ====================================================================
        st.markdown("---")
        st.subheader("💾 Export Reports")
        
        col1, col2, col3 = st.columns(3)
        
        # CSV Export
        with col1:
            csv_data = ReportExporter.export_to_csv(filtered_df)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Excel Export with multiple sheets
        with col2:
            try:
                excel_sheets = {
                    "Comments": filtered_df,
                    "Summary": ReportExporter.create_sentiment_report(df, video_info)
                }
                
                if enable_emotion:
                    excel_sheets["Emotions"] = ReportExporter.create_emotion_report(df, emotion_stats)
                
                excel_sheets["Engagement"] = ReportExporter.create_engagement_report(df)
                
                if enable_keywords:
                    excel_sheets["Keywords"] = ReportExporter.create_keyword_report(keywords_df)
                
                excel_data = ReportExporter.export_multisheet_excel(excel_sheets)
                st.download_button(
                    label="📊 Download Excel Report",
                    data=excel_data,
                    file_name=f"sentiment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error creating Excel export: {e}")
        
        # Summary Report
        with col3:
            summary_report = ReportExporter.create_sentiment_report(df, video_info)
            csv_summary = summary_report.to_csv(index=False).encode()
            st.download_button(
                label="📋 Download Summary",
                data=csv_summary,
                file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Success message
        st.success("✅ Analysis complete! Use the export buttons above to download your reports.")
    
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        st.error(f"❌ An error occurred: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    
    
</div>
""", unsafe_allow_html=True)
