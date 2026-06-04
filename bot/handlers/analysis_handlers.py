"""
Telegram bot analysis handlers
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.reply_keyboards import BotKeyboards
from services.youtube_service import YouTubeService
from services.sentiment_service import SentimentService
from services.emotion_service import EmotionService
from services.keyword_service import KeywordService
from services.topic_service import TopicService
from services.analytics_service import AnalyticsService
from config import Config

logger = logging.getLogger(__name__)


class AnalysisHandlers:
    """Handles analysis commands"""
    
    def __init__(self):
        """Initialize analysis handlers"""
        self.youtube_service = YouTubeService(Config.YOUTUBE_API_KEY)
        self.sentiment_service = SentimentService()
        self.emotion_service = EmotionService()
        self.keyword_service = KeywordService()
        self.topic_service = TopicService()
    
    async def analyze_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle video analysis"""
        try:
            # Extract URL from message
            text = update.message.text
            
            # Check if URL is provided
            if not text or ("youtube.com" not in text and "youtu.be" not in text):
                await update.message.reply_text(
                    "🔗 Please provide a valid YouTube URL:\n"
                    "/analyze https://youtube.com/watch?v=...\n\n"
                    "or\n\n"
                    "Just paste the URL in chat."
                )
                return
            
            # Show loading message
            status_msg = await update.message.reply_text("⏳ Analyzing video...")
            
            # Extract video ID
            video_id = self.youtube_service.extract_video_id(text)
            if not video_id:
                await status_msg.edit_text("❌ Invalid YouTube URL. Please check and try again.")
                return
            
            # Get video info
            video_info = self.youtube_service.get_video_info(video_id)
            if not video_info:
                await status_msg.edit_text("❌ Could not fetch video information. Please check the URL.")
                return
            
            await status_msg.edit_text("📥 Fetching comments...")
            
            # Get comments
            comments = self.youtube_service.get_comments(video_id, Config.DEFAULT_MAX_COMMENTS)
            if not comments:
                await status_msg.edit_text("❌ No comments found or unable to fetch comments.")
                return
            
            # Create DataFrame
            df = self.youtube_service.create_comments_dataframe(comments)
            
            # Analyze sentiment
            await status_msg.edit_text("😊 Analyzing sentiment...")
            df = self.sentiment_service.add_sentiment_to_dataframe(df, "text")
            
            # Analyze emotions
            await status_msg.edit_text("😌 Detecting emotions...")
            df = self.emotion_service.add_emotion_to_dataframe(df, "text")
            
            # Extract keywords
            await status_msg.edit_text("🔑 Extracting keywords...")
            df = self.keyword_service.add_keywords_to_dataframe(df, "text")
            
            # Store in context for later use
            context.user_data["current_video"] = video_info
            context.user_data["current_df"] = df
            context.user_data["video_id"] = video_id
            
            # Generate summary
            sentiment_stats = self.sentiment_service.get_statistics(df)
            emotion_stats = self.emotion_service.get_statistics(df)
            
            summary = f"""
✅ **Video Analysis Complete**

📺 **Video:** {video_info.get('title', 'N/A')[:60]}...
👤 **Channel:** {video_info.get('channel_name', 'N/A')}

📊 **Analysis Summary:**
• Total Comments Analyzed: {sentiment_stats.get('total_comments', 0)}
• 😊 Positive: {sentiment_stats.get('positive_percent', 0)}%
• 😠 Negative: {sentiment_stats.get('negative_percent', 0)}%
• 😐 Neutral: {sentiment_stats.get('neutral_percent', 0)}%

😌 **Top Emotion:** {emotion_stats.get('joy', 0)} comments with joy

👍 **Engagement:**
• Video Views: {video_info.get('view_count', 0):,}
• Video Likes: {video_info.get('like_count', 0):,}

What would you like to do next?
"""
            
            await status_msg.edit_text(summary, reply_markup=BotKeyboards.get_main_menu(), parse_mode="Markdown")
        
        except Exception as e:
            logger.error(f"Error in analyze_video: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")
    
    async def get_sentiment_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle sentiment analysis request"""
        try:
            if "current_df" not in context.user_data:
                await update.message.reply_text(
                    "📊 Please analyze a video first using /analyze <url>"
                )
                return
            
            df = context.user_data["current_df"]
            sentiment_stats = self.sentiment_service.get_statistics(df)
            
            sentiment_text = f"""
😊 **Sentiment Analysis**

📊 **Overall Breakdown:**
• Positive: {sentiment_stats.get('positive', 0)} ({sentiment_stats.get('positive_percent', 0)}%)
• Negative: {sentiment_stats.get('negative', 0)} ({sentiment_stats.get('negative_percent', 0)}%)
• Neutral: {sentiment_stats.get('neutral', 0)} ({sentiment_stats.get('neutral_percent', 0)}%)

📈 **Average Confidence Score:** {sentiment_stats.get('average_score', 0)}

💡 **Interpretation:**
"""
            
            pos_pct = sentiment_stats.get('positive_percent', 0)
            neg_pct = sentiment_stats.get('negative_percent', 0)
            
            if pos_pct > 60:
                sentiment_text += "🟢 Overall very positive audience response!"
            elif pos_pct > 40:
                sentiment_text += "🟡 Mixed with leaning positive."
            elif neg_pct > 40:
                sentiment_text += "🔴 Mixed with leaning negative."
            else:
                sentiment_text += "⚪ Balanced audience sentiment."
            
            await update.message.reply_text(
                sentiment_text,
                reply_markup=BotKeyboards.get_sentiment_keyboard(),
                parse_mode="Markdown"
            )
        
        except Exception as e:
            logger.error(f"Error in get_sentiment_analysis: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")
    
    async def get_emotion_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle emotion analysis request"""
        try:
            if "current_df" not in context.user_data:
                await update.message.reply_text(
                    "😌 Please analyze a video first using /analyze <url>"
                )
                return
            
            df = context.user_data["current_df"]
            emotion_stats = self.emotion_service.get_statistics(df)
            dominant = self.emotion_service.get_dominant_emotions(df)
            
            emotion_text = "😌 **Emotion Analysis**\n\n"
            emotion_text += "**Emotions Detected:**\n"
            
            for emotion in ["joy", "anger", "sadness", "fear", "love", "surprise"]:
                count = emotion_stats.get(emotion, 0)
                percent = emotion_stats.get(f"{emotion}_percent", 0)
                emoji = {
                    "joy": "😊", "anger": "😠", "sadness": "😢",
                    "fear": "😨", "love": "❤️", "surprise": "😮"
                }.get(emotion, "😐")
                
                emotion_text += f"{emoji} {emotion.capitalize()}: {count} ({percent}%)\n"
            
            emotion_text += f"\n📊 **Top Emotions:**\n"
            for item in dominant[:3]:
                emoji = {
                    "joy": "😊", "anger": "😠", "sadness": "😢",
                    "fear": "😨", "love": "❤️", "surprise": "😮"
                }.get(item["emotion"], "😐")
                emotion_text += f"{emoji} {item['emotion'].capitalize()}: {item['count']} ({item['percentage']}%)\n"
            
            await update.message.reply_text(
                emotion_text,
                reply_markup=BotKeyboards.get_emotion_keyboard(),
                parse_mode="Markdown"
            )
        
        except Exception as e:
            logger.error(f"Error in get_emotion_analysis: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")
    
    async def get_keywords(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle keyword extraction request"""
        try:
            if "current_df" not in context.user_data:
                await update.message.reply_text(
                    "🔑 Please analyze a video first using /analyze <url>"
                )
                return
            
            df = context.user_data["current_df"]
            keywords = self.keyword_service.get_keyword_frequency(df, Config.KEYWORD_LIMIT)
            
            keywords_text = "🔑 **Top Keywords**\n\n"
            
            for i, kw in enumerate(keywords[:10], 1):
                keywords_text += f"{i}. **{kw['keyword']}** - {kw['frequency']} mentions ({kw['percentage']}%)\n"
            
            await update.message.reply_text(
                keywords_text,
                reply_markup=BotKeyboards.get_back_keyboard(),
                parse_mode="Markdown"
            )
        
        except Exception as e:
            logger.error(f"Error in get_keywords: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")
    
    async def get_top_comments(self, update: Update, context: ContextTypes.DEFAULT_TYPE, sentiment: str = "Positive") -> None:
        """Handle top comments request"""
        try:
            if "current_df" not in context.user_data:
                await update.message.reply_text(
                    "💬 Please analyze a video first using /analyze <url>"
                )
                return
            
            df = context.user_data["current_df"]
            comments = self.sentiment_service.get_top_comments(df, sentiment, Config.TOP_COMMENTS_LIMIT)
            
            emoji = {"Positive": "😊", "Negative": "😠", "Neutral": "😐"}.get(sentiment, "💬")
            comments_text = f"{emoji} **Top {sentiment} Comments**\n\n"
            
            for i, comment in enumerate(comments[:5], 1):
                text_preview = comment["text"][:100]
                if len(comment["text"]) > 100:
                    text_preview += "..."
                
                comments_text += f"{i}. \"{text_preview}\"\n"
                comments_text += f"   👍 {comment['likes']} likes | Confidence: {comment['score']}\n\n"
            
            await update.message.reply_text(
                comments_text,
                reply_markup=BotKeyboards.get_back_keyboard(),
                parse_mode="Markdown"
            )
        
        except Exception as e:
            logger.error(f"Error in get_top_comments: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")
    
    async def get_engagement_metrics(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle engagement metrics request"""
        try:
            if "current_df" not in context.user_data:
                await update.message.reply_text(
                    "👍 Please analyze a video first using /analyze <url>"
                )
                return
            
            df = context.user_data["current_df"]
            metrics = AnalyticsService.get_engagement_metrics(df)
            
            engagement_text = "👍 **Engagement Metrics**\n\n"
            engagement_text += f"💬 Total Comments: {metrics.get('total_comments', 0)}\n"
            engagement_text += f"❤️ Total Likes: {metrics.get('total_likes', 0)}\n"
            engagement_text += f"📊 Avg Likes/Comment: {metrics.get('average_likes', 0)}\n"
            engagement_text += f"⭐ Max Likes: {metrics.get('max_likes', 0)}\n"
            engagement_text += f"📈 Engagement Rate: {metrics.get('engagement_rate', 0)}\n"
            
            if "total_replies" in metrics:
                engagement_text += f"💬 Total Replies: {metrics.get('total_replies', 0)}\n"
                engagement_text += f"📊 Avg Replies: {metrics.get('average_replies', 0)}\n"
            
            await update.message.reply_text(
                engagement_text,
                reply_markup=BotKeyboards.get_back_keyboard(),
                parse_mode="Markdown"
            )
        
        except Exception as e:
            logger.error(f"Error in get_engagement_metrics: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")
