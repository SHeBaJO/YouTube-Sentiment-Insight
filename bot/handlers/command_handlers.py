"""
Telegram bot command handlers
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import Config
from bot.keyboards.reply_keyboards import BotKeyboards

logger = logging.getLogger(__name__)

# Conversation states
WAITING_FOR_VIDEO_URL = 1


class CommandHandlers:
    """Handles bot commands"""
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        try:
            user = update.effective_user
            welcome_message = f"""
👋 Welcome {user.first_name}!

I'm your **YouTube Comment Analyzer Bot**. I can help you analyze YouTube videos and understand audience sentiment.

🎯 **What I can do:**
• 📊 Analyze sentiment of video comments
• 😊 Detect emotions (joy, anger, sadness, etc.)
• 🔑 Extract trending keywords
• 📈 Generate analytics and trends
• 💬 Find top positive/negative comments
• 👍 Analyze engagement metrics
• 📱 Analyze entire channels
• 📄 Export reports in multiple formats

🚀 Get started by analyzing a video!

Type /help for more information.
"""
            await update.message.reply_text(
                welcome_message,
                reply_markup=BotKeyboards.get_main_menu(),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Error in start handler: {e}")
            await update.message.reply_text("❌ An error occurred. Please try again.")
    
    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        try:
            help_text = """
📚 **Available Commands:**

🔍 **/analyze** - Start analyzing a YouTube video
   Usage: /analyze <video_url>

😊 **/sentiment** - Get sentiment analysis of comments
   Shows positive, negative, and neutral percentages

😌 **/emotions** - Analyze emotions in comments
   Detects: joy, anger, sadness, fear, love, surprise

🔑 **/keywords** - Extract top trending keywords

💬 **/positive** - Show top positive comments

💬 **/negative** - Show top negative comments

👍 **/likes** - Show most liked comments and engagement metrics

📈 **/trends** - Show sentiment trends over time

📱 **/channel** - Analyze multiple videos from a channel
   Usage: /channel <channel_url>

📊 **/topics** - Run topic modeling on comments

📄 **/report** - Generate downloadable report
   Formats: CSV, Excel, PDF

📥 **/download** - Download video or audio from YouTube
   Usage: /download <video_url> [video|audio]
   Or just type /download after analyzing a video

⚙️ **/settings** - Configure bot preferences

ℹ️ **/about** - About this bot

💡 **Pro Tips:**
• Paste a YouTube URL for instant analysis
• Use buttons for quick navigation
• Generate reports for sharing insights
• Analyze channels for broader insights

Need help? Contact support or use /settings.
"""
            await update.message.reply_text(
                help_text,
                parse_mode="Markdown",
                reply_markup=BotKeyboards.get_back_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in help handler: {e}")
            await update.message.reply_text("❌ An error occurred. Please try again.")
    
    @staticmethod
    async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /about command"""
        try:
            about_text = """
🤖 **YouTube Sentiment Insight Bot**

*Version:* 1.0.0

*Features:*
✅ AI-powered sentiment analysis
✅ Multi-emotion detection
✅ Keyword extraction
✅ Topic modeling
✅ Channel analytics
✅ Engagement metrics
✅ Professional reports
✅ Real-time processing

*Technology Stack:*
• Telegram Bot API
• Hugging Face Transformers
• BERTopic
• Pandas & NumPy
• YouTube API

*Developed by:* SHeBaJO

*Repository:* github.com/SHeBaJO/YouTube-Sentiment-Insight

📧 Support: Open an issue on GitHub

*Last Updated:* December 2024
"""
            await update.message.reply_text(
                about_text,
                parse_mode="Markdown",
                reply_markup=BotKeyboards.get_back_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in about handler: {e}")
            await update.message.reply_text("❌ An error occurred. Please try again.")
    
    @staticmethod
    async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /settings command"""
        try:
            settings_text = """
⚙️ **Bot Settings**

🌐 *Language:* English (More coming soon!)
📊 *Max Comments:* 500 per analysis
🎯 *Analysis Mode:* Standard
💾 *Report Format:* All formats supported

*Upcoming Settings:*
• Language preferences
• Custom analysis depth
• Notification preferences
• Data retention settings

For now, these settings are fixed. Future updates will allow customization.
"""
            await update.message.reply_text(
                settings_text,
                parse_mode="Markdown",
                reply_markup=BotKeyboards.get_back_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in settings handler: {e}")
            await update.message.reply_text("❌ An error occurred. Please try again.")
