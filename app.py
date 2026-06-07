"""
Streamlit dashboard for YouTube comment sentiment analysis.
"""
import logging
from datetime import datetime

import pandas as pd
import streamlit as st

from src.analytics.keywords import analyze_keywords, get_keyword_frequency_distribution
from src.analytics.topics import add_topics_to_dataframe, get_topic_summary
from src.analytics.trends import TrendAnalyzer
from src.config import config
from src.dashboard.export import ReportExporter
from src.dashboard.visualizations import DashboardVisualizations
from src.models.emotion import EmotionDetector, add_emotion_to_dataframe, get_emotion_statistics
from src.models.sentiment import SentimentAnalyzer, add_sentiment_to_dataframe, get_sentiment_statistics
from src.utils.youtube_api import YouTubeCommentExtractor, create_comments_dataframe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="YouTube Sentiment Insight",
    page_icon="YT",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stButton > button {
            background-color: #d71920;
            color: white;
            border-radius: 8px;
            font-weight: 700;
            border: 0;
        }
        .stMetric {
            background: rgba(250, 250, 250, 0.04);
            border: 1px solid rgba(250, 250, 250, 0.08);
            border-radius: 8px;
            padding: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("YouTube Sentiment Insight")
st.caption("Analyze YouTube comments with sentiment, emotion, keyword, and engagement insights.")

st.sidebar.header("Analysis Settings")

if config is None:
    st.error(
        "YouTube API key not found. Add YOUTUBE_API_KEY to your environment or "
        "to .streamlit/secrets.toml."
    )
    st.stop()

max_comments = st.sidebar.slider(
    "Maximum comments",
    min_value=10,
    max_value=500,
    value=100,
    step=10,
)

st.sidebar.subheader("Analysis Modules")
enable_emotion = st.sidebar.checkbox("Emotion detection", value=True)
enable_keywords = st.sidebar.checkbox("Keyword analysis", value=True)
enable_trends = st.sidebar.checkbox("Trend analysis", value=True)
enable_topics = st.sidebar.checkbox("Topic modeling", value=False)

st.divider()
st.subheader("Video")

youtube_url = st.text_input(
    "YouTube video URL",
    placeholder="https://www.youtube.com/watch?v=...",
)

analyze_button = st.button("Analyze comments", use_container_width=True)

with st.expander("📥 Download Video/Audio"):
    dl_format = st.selectbox("Format", ["Video (MP4)", "Audio (M4A)"])
    if st.button("Download File", use_container_width=True, key="download_video_btn"):
        if not youtube_url:
            st.error("Please enter a YouTube video URL.")
        else:
            with st.spinner("Downloading from YouTube..."):
                import os
                from services.download_service import DownloadService
                fmt = "audio" if "Audio" in dl_format else "video"
                res = DownloadService.download(youtube_url, format_type=fmt)
                if res.get("success"):
                    filepath = res["filepath"]
                    title = res["title"]
                    try:
                        with open(filepath, "rb") as f:
                            file_bytes = f.read()
                        st.success(f"Successfully downloaded: {title}")
                        st.download_button(
                            label="Save File to Device",
                            data=file_bytes,
                            file_name=os.path.basename(filepath),
                            mime="video/mp4" if fmt == "video" else "audio/mp4",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error reading downloaded file: {e}")
                    finally:
                        if os.path.exists(filepath):
                            try:
                                os.remove(filepath)
                            except Exception as e:
                                logger.error(f"Error cleaning up file: {e}")
                else:
                    st.error(f"Download failed: {res.get('error')}")

if analyze_button:
    if not youtube_url:
        st.error("Please enter a YouTube video URL.")
        st.stop()

    try:
        extractor = YouTubeCommentExtractor(config.YOUTUBE_API_KEY)
        video_id = extractor.extract_video_id(youtube_url)

        if not video_id:
            st.error("Invalid YouTube URL. Please check the link and try again.")
            st.stop()

        with st.spinner("Fetching video information..."):
            video_info = extractor.get_video_info(video_id)

        if not video_info:
            st.error("Could not fetch video information. The video may be private or unavailable.")
            st.stop()

        st.success(f"Video found: {video_info.get('title', 'Unknown title')}")

        progress_bar = st.progress(0)
        status_text = st.empty()

        with st.spinner("Fetching comments..."):
            def progress_callback(progress):
                progress_bar.progress(progress)
                status_text.text(f"Fetched {int(progress * max_comments)}/{max_comments} comments")

            comments_data = extractor.fetch_comments(
                video_id,
                max_comments=max_comments,
                progress_callback=progress_callback,
            )

        if not comments_data:
            st.error("No comments found for this video.")
            st.stop()

        df = create_comments_dataframe(comments_data)

        with st.spinner("Analyzing sentiment..."):
            sentiment_analyzer = SentimentAnalyzer()
            df = add_sentiment_to_dataframe(df, sentiment_analyzer, text_column="text")

        emotion_stats = None
        if enable_emotion:
            with st.spinner("Detecting emotions..."):
                emotion_detector = EmotionDetector()
                df = add_emotion_to_dataframe(df, emotion_detector, text_column="text")
                emotion_stats = get_emotion_statistics(df)

        keywords_df = pd.DataFrame()
        if enable_keywords:
            with st.spinner("Extracting keywords..."):
                analyze_keywords(df, text_column="text", top_n=20)
                keywords_df = get_keyword_frequency_distribution(df, text_column="text", top_n=15)

        if enable_topics:
            with st.spinner("Modeling topics..."):
                df = add_topics_to_dataframe(df, df["text"].tolist())

        st.divider()
        st.subheader("Summary")

        sentiment_stats = get_sentiment_statistics(df)
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Comments", sentiment_stats["total_comments"])
        col2.metric("Positive", f"{sentiment_stats['positive_pct']:.1f}%")
        col3.metric("Negative", f"{sentiment_stats['negative_pct']:.1f}%")
        col4.metric("Neutral", f"{sentiment_stats['neutral_pct']:.1f}%")
        col5.metric("Avg confidence", f"{sentiment_stats['average_confidence']:.2f}")

        st.subheader("Engagement")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total likes", int(df["likes"].sum()))
        col2.metric("Average likes", f"{df['likes'].mean():.1f}")
        col3.metric("Top likes", int(df["likes"].max()))
        col4.metric("Average replies", f"{df.get('reply_count', pd.Series([0])).mean():.1f}")

        st.divider()
        st.subheader("Visualizations")

        sentiment_counts = df["sentiment"].value_counts().to_dict()
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                DashboardVisualizations.sentiment_pie_chart(sentiment_counts),
                use_container_width=True,
            )

        with col2:
            sentiment_df = pd.DataFrame(
                {
                    "Sentiment": list(sentiment_counts.keys()),
                    "Count": list(sentiment_counts.values()),
                }
            )
            st.plotly_chart(
                DashboardVisualizations.sentiment_bar_chart(sentiment_df),
                use_container_width=True,
            )

        st.subheader("Word Cloud")
        st.pyplot(DashboardVisualizations.wordcloud(df["text"].tolist()), use_container_width=True)

        st.subheader("Engagement Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                DashboardVisualizations.likes_distribution_chart(df),
                use_container_width=True,
            )
        with col2:
            st.plotly_chart(
                DashboardVisualizations.sentiment_vs_likes_scatter(df),
                use_container_width=True,
            )

        if enable_keywords and not keywords_df.empty:
            st.divider()
            st.subheader("Keywords")
            st.plotly_chart(
                DashboardVisualizations.keyword_bar_chart(keywords_df, top_n=15),
                use_container_width=True,
            )
            st.dataframe(keywords_df, use_container_width=True)

        if enable_emotion and emotion_stats:
            st.divider()
            st.subheader("Emotion Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Dominant emotion: **{emotion_stats['dominant_emotion'].capitalize()}**")
                st.write(f"Average confidence: **{emotion_stats['average_confidence']:.2f}**")
            with col2:
                st.plotly_chart(
                    DashboardVisualizations.emotion_distribution_chart(
                        emotion_stats["emotion_distribution"]
                    ),
                    use_container_width=True,
                )

        if enable_trends:
            st.divider()
            st.subheader("Sentiment Trends")
            daily_trends = TrendAnalyzer.daily_sentiment_trends(df)
            trend_summary = TrendAnalyzer.get_trend_summary(df)

            st.plotly_chart(
                DashboardVisualizations.sentiment_trend_chart(daily_trends),
                use_container_width=True,
            )

            col1, col2, col3 = st.columns(3)
            col1.write(f"Time span: **{trend_summary['time_span_days']} days**")
            col2.write(f"Trend: **{trend_summary['sentiment_trend'].upper()}**")
            col3.write(f"Change: **{trend_summary['trend_change_pct']:.1f}%**")

        if enable_topics and "topic" in df.columns:
            st.divider()
            st.subheader("Topics")
            topics_df = get_topic_summary(df)

            if not topics_df.empty:
                st.plotly_chart(
                    DashboardVisualizations.topic_distribution_chart(topics_df),
                    use_container_width=True,
                )
                st.dataframe(topics_df, use_container_width=True)

        st.divider()
        st.subheader("Comments")

        filter_col1, filter_col2 = st.columns([2, 1])
        with filter_col1:
            filter_option = st.selectbox("Filter by sentiment", ["All", "Positive", "Negative", "Neutral"])
        with filter_col2:
            sort_by = st.selectbox("Sort by", ["Likes descending", "Date newest", "Confidence"])

        filtered_df = df.copy() if filter_option == "All" else df[df["sentiment"] == filter_option].copy()

        if sort_by == "Likes descending":
            filtered_df = filtered_df.sort_values("likes", ascending=False)
        elif sort_by == "Date newest":
            filtered_df = filtered_df.sort_values("published_at", ascending=False)
        else:
            filtered_df = filtered_df.sort_values("confidence", ascending=False)

        st.dataframe(filtered_df, use_container_width=True)

        st.divider()
        st.subheader("Export")

        col1, col2, col3 = st.columns(3)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        with col1:
            csv_data = ReportExporter.export_to_csv(filtered_df)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"sentiment_analysis_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with col2:
            try:
                excel_sheets = {
                    "Comments": filtered_df,
                    "Summary": ReportExporter.create_sentiment_report(df, video_info),
                    "Engagement": ReportExporter.create_engagement_report(df),
                }

                if enable_emotion and emotion_stats:
                    excel_sheets["Emotions"] = ReportExporter.create_emotion_report(df, emotion_stats)
                if enable_keywords and not keywords_df.empty:
                    excel_sheets["Keywords"] = ReportExporter.create_keyword_report(keywords_df)

                excel_data = ReportExporter.export_multisheet_excel(excel_sheets)
                st.download_button(
                    label="Download Excel report",
                    data=excel_data,
                    file_name=f"sentiment_report_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )
            except Exception as exc:
                st.error(f"Error creating Excel export: {exc}")

        with col3:
            summary_report = ReportExporter.create_sentiment_report(df, video_info)
            st.download_button(
                label="Download summary",
                data=summary_report.to_csv(index=False).encode(),
                file_name=f"summary_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.success("Analysis complete.")

    except Exception as exc:
        logger.error("Error during analysis: %s", exc)
        st.error(f"An error occurred: {exc}")
