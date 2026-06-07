# YouTube Sentiment Insight

YouTube Sentiment Insight is a Python project for analyzing YouTube comments with NLP, engagement metrics, and interactive reporting. It includes a Streamlit dashboard for visual analysis and a Telegram bot entry point for chat-based analysis workflows.

## Features

- Fetch YouTube video comments with the YouTube Data API v3
- Run transformer-based sentiment analysis
- Detect emotions with Hugging Face models
- Extract keywords and summarize discussion themes
- Analyze engagement through likes, replies, and comment trends
- Visualize results with Plotly, Matplotlib, and word clouds
- Export analysis data to CSV and Excel
- Optional Telegram bot interface for command-based analysis

## Project Structure

```text
.
├── app.py                     # Streamlit dashboard entry point
├── main.py                    # Telegram bot entry point
├── src/
│   ├── analytics/             # Keyword, trend, and topic analysis
│   ├── dashboard/             # Charts and export helpers
│   ├── models/                # Sentiment and emotion models
│   └── utils/                 # YouTube API utilities
├── bot/                       # Telegram handlers and keyboards
├── config/                    # Telegram bot configuration
├── tests/                     # Pytest test suite
├── .github/workflows/         # GitHub Actions CI
├── .env.example               # Environment variable template
├── requirements.txt           # Python dependencies
└── README.md
```

## Requirements

- Python 3.10 or newer
- YouTube Data API v3 key
- Telegram bot token, only if you want to run the Telegram bot

The first analysis can take extra time because transformer models are downloaded and cached locally.

## Installation

```bash
git clone https://github.com/SHeBaJO/YouTube-Sentiment-Insight.git
cd YouTube-Sentiment-Insight

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

For macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Set the required values:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

For Streamlit Cloud or local Streamlit secrets, you can also create `.streamlit/secrets.toml`:

```toml
YOUTUBE_API_KEY = "your_youtube_api_key_here"
```

Never commit real API keys or bot tokens.

## Running The Dashboard

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, paste a YouTube video URL, choose the analysis options, and run the analysis.

## Running The Telegram Bot

Make sure both `YOUTUBE_API_KEY` and `TELEGRAM_BOT_TOKEN` are configured, then run:

```bash
python main.py
```

Supported bot commands include:

- `/start`
- `/help`
- `/about`
- `/settings`
- `/analyze <youtube_video_url>`
- `/sentiment`
- `/emotions`
- `/keywords`
- `/likes`

## Testing

```bash
pytest tests/ -v
```

Some model-related tests may skip if transformer models cannot be loaded in the current environment.

## Notes On Scope

This project is upload-ready as an analysis application, but it is still best treated as an educational or prototype analytics tool rather than a production SaaS. For production use, add persistent storage, stronger rate limiting, deployment secrets management, and monitoring.

## Security

- Credentials are read from environment variables or Streamlit secrets.
- `.env` and Streamlit secret files are ignored by git.
- Generated reports and local model/cache files are excluded from the repository.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Created by [SHeBaJO](https://github.com/SHeBaJO).
