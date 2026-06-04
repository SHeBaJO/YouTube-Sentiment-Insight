"""
Telegram bot keyboards and inline buttons
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


class BotKeyboards:
    """Collection of Telegram bot keyboards"""
    
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        """Get main menu keyboard"""
        keyboard = [
            [KeyboardButton("🔍 Analyze Video")],
            [KeyboardButton("📊 Statistics"), KeyboardButton("😊 Sentiment")],
            [KeyboardButton("🔑 Keywords"), KeyboardButton("💬 Top Comments")],
            [KeyboardButton("😌 Emotions"), KeyboardButton("📈 Trends")],
            [KeyboardButton("📱 Channel"), KeyboardButton("📄 Report")],
            [KeyboardButton("ℹ️ Help"), KeyboardButton("⚙️ Settings")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def get_sentiment_keyboard() -> InlineKeyboardMarkup:
        """Get sentiment analysis options keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("😊 Positive", callback_data="sentiment_positive"),
                InlineKeyboardButton("😠 Negative", callback_data="sentiment_negative")
            ],
            [
                InlineKeyboardButton("😐 Neutral", callback_data="sentiment_neutral"),
                InlineKeyboardButton("📊 Summary", callback_data="sentiment_summary")
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_likes_keyboard() -> InlineKeyboardMarkup:
        """Get likes analysis options keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("👍 Most Liked", callback_data="likes_top"),
                InlineKeyboardButton("📊 Statistics", callback_data="likes_stats")
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_report_keyboard() -> InlineKeyboardMarkup:
        """Get report format selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📋 CSV", callback_data="report_csv"),
                InlineKeyboardButton("📊 Excel", callback_data="report_xlsx")
            ],
            [
                InlineKeyboardButton("📄 PDF", callback_data="report_pdf"),
                InlineKeyboardButton("⬅️ Cancel", callback_data="back_to_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_yes_no_keyboard() -> InlineKeyboardMarkup:
        """Get yes/no confirmation keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Yes", callback_data="confirm_yes"),
                InlineKeyboardButton("❌ No", callback_data="confirm_no")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_back_keyboard() -> InlineKeyboardMarkup:
        """Get back button keyboard"""
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_emotion_keyboard() -> InlineKeyboardMarkup:
        """Get emotion analysis options keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("😊 Joy", callback_data="emotion_joy"),
                InlineKeyboardButton("😠 Anger", callback_data="emotion_anger")
            ],
            [
                InlineKeyboardButton("😢 Sadness", callback_data="emotion_sadness"),
                InlineKeyboardButton("😨 Fear", callback_data="emotion_fear")
            ],
            [
                InlineKeyboardButton("❤️ Love", callback_data="emotion_love"),
                InlineKeyboardButton("😮 Surprise", callback_data="emotion_surprise")
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_channel_keyboard() -> InlineKeyboardMarkup:
        """Get channel analysis options keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📺 Recent Videos", callback_data="channel_videos"),
                InlineKeyboardButton("📊 Overall Stats", callback_data="channel_stats")
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_pagination_keyboard(page: int, total_pages: int, base_callback: str) -> InlineKeyboardMarkup:
        """
        Get pagination keyboard
        
        Args:
            page: Current page number
            total_pages: Total number of pages
            base_callback: Base callback prefix
            
        Returns:
            Pagination keyboard
        """
        keyboard = []
        
        if page > 1:
            keyboard.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"{base_callback}_prev"))
        
        keyboard.append(InlineKeyboardButton(f"Page {page}/{total_pages}", callback_data="noop"))
        
        if page < total_pages:
            keyboard.append(InlineKeyboardButton("Next ➡️", callback_data=f"{base_callback}_next"))
        
        return InlineKeyboardMarkup([keyboard, [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]])
    
    @staticmethod
    def get_language_keyboard() -> InlineKeyboardMarkup:
        """Get language selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
                InlineKeyboardButton("🇮🇳 Hindi", callback_data="lang_hi")
            ],
            [
                InlineKeyboardButton("🇲🇱 Malayalam", callback_data="lang_ml"),
                InlineKeyboardButton("🇮🇳 Tamil", callback_data="lang_ta")
            ],
            [
                InlineKeyboardButton("🇮🇳 Telugu", callback_data="lang_te"),
                InlineKeyboardButton("🇪🇸 Spanish", callback_data="lang_es")
            ],
            [
                InlineKeyboardButton("🇫🇷 French", callback_data="lang_fr"),
                InlineKeyboardButton("🇩🇪 German", callback_data="lang_de")
            ],
            [
                InlineKeyboardButton("🇸🇦 Arabic", callback_data="lang_ar"),
                InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
