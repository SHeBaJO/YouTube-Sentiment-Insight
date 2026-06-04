"""
Main entry point for YouTube Sentiment Analysis Telegram Bot
"""
import logging
import os
from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from config import Config, get_config
from bot.handlers.command_handlers import CommandHandlers
from bot.handlers.message_handlers import MessageHandlers, CallbackHandlers

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot"""
    try:
        # Validate configuration
        config = get_config()
        
        # Create the Application
        app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Initialize handlers
        command_handlers = CommandHandlers()
        message_handlers = MessageHandlers()
        callback_handlers = CallbackHandlers()
        
        # Command handlers
        app.add_handler(CommandHandler("start", command_handlers.start))
        app.add_handler(CommandHandler("help", command_handlers.help_command))
        app.add_handler(CommandHandler("about", command_handlers.about))
        app.add_handler(CommandHandler("settings", command_handlers.settings))
        
        # Analysis command handlers
        app.add_handler(CommandHandler("analyze", message_handlers.analysis.analyze_video))
        app.add_handler(CommandHandler("sentiment", message_handlers.analysis.get_sentiment_analysis))
        app.add_handler(CommandHandler("emotions", message_handlers.analysis.get_emotion_analysis))
        app.add_handler(CommandHandler("keywords", message_handlers.analysis.get_keywords))
        app.add_handler(CommandHandler("likes", message_handlers.analysis.get_engagement_metrics))
        
        # Message handler for text messages
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.handle_message))
        
        # Callback handler for inline buttons
        app.add_handler(CallbackQueryHandler(callback_handlers.handle_callback))
        
        # Error handler
        app.add_error_handler(error_handler)
        
        # Start the bot
        logger.info("Starting YouTube Sentiment Analysis Bot...")
        app.run_polling()
    
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)


async def error_handler(update, context):
    """Handle errors"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again or contact support.\n\n"
                "Error has been logged for debugging."
            )
        except Exception as e:
            logger.error(f"Error sending error message: {e}")


if __name__ == "__main__":
    main()
