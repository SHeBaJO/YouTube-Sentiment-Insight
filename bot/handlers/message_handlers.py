"""
Telegram bot message and callback handlers
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.handlers.command_handlers import CommandHandlers
from bot.handlers.analysis_handlers import AnalysisHandlers
from bot.keyboards.reply_keyboards import BotKeyboards
from services.youtube_service import YouTubeService
from services.sentiment_service import SentimentService
from config import Config

logger = logging.getLogger(__name__)


class MessageHandlers:
    """Handles regular messages from users"""
    
    def __init__(self):
        """Initialize message handlers"""
        self.analysis = AnalysisHandlers()
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular messages"""
        try:
            text = update.message.text
            
            # Check for YouTube URL in message
            if "youtube.com" in text or "youtu.be" in text:
                await self.analysis.analyze_video(update, context)
                return
            
            # Handle button presses from main menu
            if text == "🔍 Analyze Video":
                msg = await update.message.reply_text("🔗 Send me a YouTube video link or URL:")
                context.user_data["waiting_for_url"] = True
            
            elif text == "😊 Sentiment":
                await self.analysis.get_sentiment_analysis(update, context)
            
            elif text == "😌 Emotions":
                await self.analysis.get_emotion_analysis(update, context)
            
            elif text == "🔑 Keywords":
                await self.analysis.get_keywords(update, context)
            
            elif text == "💬 Top Comments":
                await update.message.reply_text(
                    "💬 Which sentiment would you like to see?\n",
                    reply_markup=BotKeyboards.get_sentiment_keyboard()
                )
            
            elif text == "👍 Likes":
                await self.analysis.get_engagement_metrics(update, context)
            
            elif text == "📊 Statistics":
                if "current_video" in context.user_data:
                    video = context.user_data["current_video"]
                    df = context.user_data["current_df"]
                    stats = f"""
📊 **Video Statistics**

🎬 **Video Info:**
• Title: {video.get('title', 'N/A')[:50]}...
• Channel: {video.get('channel_name', 'N/A')}
• Views: {video.get('view_count', 0):,}
• Likes: {video.get('like_count', 0):,}
• Comments: {video.get('comment_count', 0):,}

📈 **Analysis Stats:**
• Comments Analyzed: {len(df)}
• Avg Comment Length: {df['text'].str.len().mean():.0f} chars
"""
                    await update.message.reply_text(stats, parse_mode="Markdown")
                else:
                    await update.message.reply_text("📊 Please analyze a video first!")
            
            elif text == "📈 Trends":
                await update.message.reply_text(
                    "📈 Sentiment trends will be available soon!"
                )
            
            elif text == "📱 Channel":
                await update.message.reply_text(
                    "📱 Please provide a YouTube channel URL:\n"
                    "https://youtube.com/@channelname"
                )
            
            elif text == "📄 Report":
                if "current_df" in context.user_data:
                    await update.message.reply_text(
                        "📄 Select report format:",
                        reply_markup=BotKeyboards.get_report_keyboard()
                    )
                else:
                    await update.message.reply_text("📄 Please analyze a video first!")
            
            elif text == "ℹ️ Help":
                await CommandHandlers.help_command(update, context)
            
            elif text == "⚙️ Settings":
                await CommandHandlers.settings(update, context)
            
            else:
                # Default response for unknown input
                if context.user_data.get("waiting_for_url"):
                    context.user_data["waiting_for_url"] = False
                    await update.message.reply_text(
                        "❌ That doesn't look like a valid YouTube URL.\n\n"
                        "Please provide a link like:\n"
                        "https://www.youtube.com/watch?v=...\n\n"
                        "or\n\n"
                        "https://youtu.be/..."
                    )
                else:
                    await update.message.reply_text(
                        "🤔 I didn't understand that. Please use the menu buttons or send a YouTube URL.",
                        reply_markup=BotKeyboards.get_main_menu()
                    )
        
        except Exception as e:
            logger.error(f"Error in handle_message: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")


class CallbackHandlers:
    """Handles callback queries from inline buttons"""
    
    def __init__(self):
        """Initialize callback handlers"""
        self.analysis = AnalysisHandlers()
        self.sentiment_service = SentimentService()
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle callback queries"""
        try:
            query = update.callback_query
            await query.answer()
            
            callback_data = query.data
            
            # Main menu callbacks
            if callback_data == "back_to_main":
                await query.edit_message_text(
                    "👋 What would you like to do?",
                    reply_markup=BotKeyboards.get_main_menu()
                )
            
            # Sentiment callbacks
            elif callback_data == "sentiment_summary":
                await self.analysis.get_sentiment_analysis(update, context)
            
            elif callback_data.startswith("sentiment_"):
                sentiment = callback_data.replace("sentiment_", "").capitalize()
                await self.analysis.get_top_comments(update, context, sentiment)
            
            # Emotion callbacks
            elif callback_data.startswith("emotion_"):
                emotion = callback_data.replace("emotion_", "")
                await query.edit_message_text(
                    f"😌 Emotion analysis for {emotion} coming soon!"
                )
            
            # Likes callbacks
            elif callback_data == "likes_top":
                if "current_df" in context.user_data:
                    df = context.user_data["current_df"]
                    df_sorted = df.nlargest(5, "likes")
                    
                    likes_text = "👍 **Most Liked Comments:**\n\n"
                    for i, (_, row) in enumerate(df_sorted.iterrows(), 1):
                        text_preview = row["text"][:80]
                        if len(row["text"]) > 80:
                            text_preview += "..."
                        likes_text += f"{i}. \"{text_preview}\"\n   ❤️ {row['likes']} likes\n\n"
                    
                    await query.edit_message_text(
                        likes_text,
                        reply_markup=BotKeyboards.get_back_keyboard(),
                        parse_mode="Markdown"
                    )
                else:
                    await query.edit_message_text("Please analyze a video first!")
            
            # Report callbacks
            elif callback_data.startswith("report_"):
                report_format = callback_data.replace("report_", "").upper()
                await query.edit_message_text(
                    f"📄 Generating {report_format} report...\n\n"
                    "This feature is coming soon!"
                )
            
            # Language callbacks
            elif callback_data.startswith("lang_"):
                lang = callback_data.replace("lang_", "")
                await query.edit_message_text(
                    f"🌐 Language set to {lang.upper()}\n\n"
                    "(Multilingual support coming soon!)"
                )
            
            # Confirmation callbacks
            elif callback_data == "confirm_yes":
                await query.edit_message_text(
                    "✅ Action confirmed!"
                )
            
            elif callback_data == "confirm_no":
                await query.edit_message_text(
                    "❌ Action cancelled."
                )
            
            else:
                await query.answer("Unknown action", show_alert=False)
        
        except Exception as e:
            logger.error(f"Error in handle_callback: {e}")
            try:
                await update.callback_query.answer(f"Error: {str(e)[:50]}", show_alert=True)
            except:
                pass
