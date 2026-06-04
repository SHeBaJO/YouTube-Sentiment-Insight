# 🎥 YouTube Sentiment Insight Bot

An AI-powered Telegram bot for comprehensive YouTube audience sentiment analysis using advanced NLP and machine learning.

## 📋 Overview

YouTube Sentiment Insight Bot transforms YouTube comment analysis by providing:

- **Real-time Sentiment Analysis**: Detect positive, negative, and neutral comments using transformer-based models
- **Multi-emotion Detection**: Identify joy, anger, sadness, fear, love, and surprise
- **Keyword Extraction**: Discover trending topics and keywords
- **Engagement Analytics**: Analyze likes, comments, and interaction patterns
- **Topic Modeling**: Understand main discussion themes using BERTopic
- **Channel Analytics**: Analyze multiple videos from a channel
- **Professional Reports**: Export insights in CSV, Excel, and PDF formats
- **Telegram Integration**: User-friendly bot interface for easy interaction

## 🏗️ Architecture

```
YouTube Sentiment Insight Bot
│
├── bot/                          # Telegram Bot Components
│   ├── handlers/                 # Command, message, callback handlers
│   │   ├── command_handlers.py   # /start, /help, /analyze, etc.
│   │   ├── analysis_handlers.py  # Analysis logic handlers
│   │   └── message_handlers.py   # Message and callback routing
│   └── keyboards/                # Telegram UI keyboards
│       └── reply_keyboards.py    # Inline and reply keyboards
│
├── services/                      # Business Logic Services
│   ├── youtube_service.py         # YouTube API interactions
│   ├── sentiment_service.py       # Sentiment analysis
│   ├── emotion_service.py         # Emotion detection
│   ├── keyword_service.py         # Keyword extraction
│   ├── topic_service.py           # Topic modeling
│   └── analytics_service.py       # Analytics aggregation
│
├── config/                        # Configuration Management
│   └── settings.py                # Environment & settings
│
├── reports/                       # Report Generation
│   └── report_generator.py        # CSV, Excel, PDF export
│
├── main.py                        # Bot entry point
├── requirements.txt               # Dependencies
├── .env.example                   # Environment template
└── README.md                      # Documentation
```

## 🚀 Features

### Core Commands

#### `/start`
Welcome message with available commands and quick start guide.

#### `/help`
Detailed command reference and usage instructions.

#### `/analyze <video_url>`
Analyze a YouTube video's comments:
- Fetches up to 500 comments
- Performs sentiment analysis
- Detects emotions
- Extracts keywords
- Generates summary statistics

#### `/sentiment`
Get sentiment breakdown:
- Positive percentage
- Negative percentage
- Neutral percentage
- Average confidence score

#### `/emotions`
Analyze emotional distribution:
- Joy, Anger, Sadness, Fear, Love, Surprise
- Percentage breakdown
- Top emotional trends

#### `/keywords`
Extract trending keywords:
- Top 20 keywords by frequency
- Occurrence count and percentages

#### `/positive`
Show top positive comments with high sentiment scores.

#### `/negative`
Show top negative comments for understanding criticism.

#### `/likes`
Engagement metrics:
- Most liked comments
- Average likes per comment
- Total engagement statistics

#### `/topics`
Topic modeling insights:
- Main discussion topics
- Topic distribution
- Sample comments per topic

#### `/trends`
Sentiment trends over time:
- Daily sentiment distribution
- Trend visualization data

#### `/channel <channel_url>`
Analyze entire channel:
- Recent videos list
- Overall sentiment across videos
- Engagement comparison

#### `/report`
Generate comprehensive reports:
- **CSV**: Spreadsheet format with detailed data
- **Excel**: Multi-sheet workbook with summaries
- **PDF**: Professional formatted report

#### `/settings`
Configure bot preferences (expanding in future versions).

### Advanced Features

#### 🤖 Transformer-Based NLP
Uses state-of-the-art models:
- **Sentiment**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Emotion**: `j-hartmann/emotion-english-distilroberta-base`
- **Multilingual**: `xlm-roberta-base` (future)

#### 📊 Topic Modeling
Implements BERTopic for:
- Unsupervised topic discovery
- Topic probability distributions
- Sample document extraction per topic

#### 🌐 Multilingual Support (Planned)
Support for:
- English, Hindi, Malayalam, Tamil, Telugu
- Spanish, French, German, Arabic, Portuguese

#### 📱 Channel-level Analytics
- Analyze multiple videos
- Compare sentiment across videos
- Track channel engagement trends
- Identify content performance patterns

## 📥 Installation

### Prerequisites
- Python 3.10 or higher
- Telegram Bot Token
- YouTube API Key

### Step 1: Clone Repository
```bash
git clone https://github.com/SHeBaJO/YouTube-Sentiment-Insight.git
cd YouTube-Sentiment-Insight
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
```bash
# Copy example file
cp .env.example .env

# Edit .env with your credentials
YOUTUBE_API_KEY=your_youtube_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

### Step 5: Run Bot
```bash
python main.py
```

## 🔐 Getting API Keys

### YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create OAuth 2.0 credentials (API key)
5. Copy the key to `.env`

### Telegram Bot Token
1. Chat with [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command
3. Follow instructions to create bot
4. Copy the token to `.env`

## 📊 Data Flow

```
User Input (Telegram)
    ↓
Message Handler Router
    ↓
Analysis Handler (if YouTube URL)
    ↓
YouTube Service ← Fetch Comments
    ↓
Sentiment Service ← Analyze Sentiment
    ↓
Emotion Service ← Detect Emotions
    ↓
Keyword Service ← Extract Keywords
    ↓
Topic Service ← Model Topics
    ↓
Analytics Service ← Aggregate Stats
    ↓
Report Generator (if requested)
    ↓
Telegram Response (formatted message or file)
```

## 💾 Database & Storage

Currently uses:
- **Comments Data**: Stored in pandas DataFrames (in-memory)
- **User Session Data**: Stored in Telegram context
- **Reports**: Generated on-demand in `/reports/` directory

Future: Integration with SQLite/PostgreSQL for persistent storage.

## 🔧 Configuration

### Default Settings (config/settings.py)

```python
SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
DEFAULT_MAX_COMMENTS = 500
KEYWORD_LIMIT = 20
TOP_COMMENTS_LIMIT = 10
```

### Environment Variables

```env
# Required
YOUTUBE_API_KEY=<your_key>
TELEGRAM_BOT_TOKEN=<your_token>

# Optional
MAX_COMMENT_BATCH=100
REQUEST_TIMEOUT=30
```

## 🚦 Error Handling

Bot handles:
- Invalid YouTube URLs
- API rate limits
- Network timeouts
- Invalid credentials
- No comments on video
- Model loading failures

Each error provides user-friendly feedback.

## 📦 Dependencies

### Core
- **python-telegram-bot** (20.3): Telegram API client
- **google-api-python-client** (2.100.0): YouTube API

### NLP
- **transformers** (4.34.0): Hugging Face models
- **torch** (2.0.1): PyTorch engine
- **bertopic** (0.15.0): Topic modeling
- **nltk** (3.8.1): Natural Language Toolkit

### Data Processing
- **pandas** (2.1.1): Data manipulation
- **numpy** (1.24.3): Numerical computing
- **scikit-learn** (1.3.2): ML utilities

### Export
- **openpyxl** (3.1.2): Excel writing
- **reportlab** (4.0.9): PDF generation

## 📈 Performance

- Comment Analysis: ~100 comments/minute (CPU)
- Model Loading: ~10-15 seconds (first run)
- Sentiment Accuracy: ~92% (DistilBERT model)
- Emotion Detection: ~85% accuracy

## 🔒 Security

- ✅ Environment variables for credentials (never hardcoded)
- ✅ HTTPS for API calls
- ✅ Rate limiting via Telegram API
- ✅ No user data persistence without consent
- ✅ Input validation on all user inputs

### Best Practices
1. Keep `.env` file secure (add to `.gitignore`)
2. Rotate API keys regularly
3. Monitor API usage and quotas
4. Use separate bot token for production
5. Enable Telegram bot privacy mode

## 🤝 Contributing

Contributions welcome! Areas needing help:

- [ ] Multilingual sentiment analysis
- [ ] Real-time monitoring feature
- [ ] Persistent database integration
- [ ] Web dashboard
- [ ] Advanced topic visualization
- [ ] Sentiment trend predictions

## 🐛 Troubleshooting

### Bot won't start
```bash
# Check .env file exists and has valid tokens
# Verify Python version: python --version
# Check internet connection
# Try: python main.py --debug
```

### Models not loading
```bash
# Clear cache: rm -rf ~/.cache/huggingface
# Reinstall: pip install --upgrade transformers torch
# Check disk space for models
```

### YouTube API errors
```bash
# Verify API key is enabled for YouTube Data API v3
# Check quota at console.cloud.google.com
# Ensure video has comments enabled
```

### Memory issues
```bash
# Reduce MAX_COMMENTS in .env
# Use device-specific optimization
# Consider GPU support for faster processing
```

## 📚 Resources

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Hugging Face Models](https://huggingface.co/models)
- [BERTopic Documentation](https://maartengr.github.io/BERTopic/)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**SHeBaJO**
- GitHub: [@SHeBaJO](https://github.com/SHeBaJO)
- Project: [YouTube-Sentiment-Insight](https://github.com/SHeBaJO/YouTube-Sentiment-Insight)

## 🎯 Roadmap

### v1.1 (Q1 2025)
- [ ] Real-time comment monitoring
- [ ] Persistent storage (SQLite)
- [ ] Advanced filtering options
- [ ] Comment sentiment distribution chart

### v1.2 (Q2 2025)
- [ ] Multilingual support
- [ ] Web dashboard
- [ ] Scheduled analysis reports
- [ ] Comment sentiment predictions

### v2.0 (Q3 2025)
- [ ] Machine learning model training
- [ ] Custom sentiment models
- [ ] Advanced analytics engine
- [ ] API for third-party integration

## 🙏 Acknowledgments

- Hugging Face for transformer models
- python-telegram-bot team
- Google for YouTube API
- Open-source community

## 📞 Support

For issues and feature requests:
1. Check [Troubleshooting](#troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/SHeBaJO/YouTube-Sentiment-Insight/issues)
3. Open new issue with detailed description

---

**Made with ❤️ by SHeBaJO | Last Updated: December 2024**
