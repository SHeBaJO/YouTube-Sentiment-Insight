# 🎥 YouTube Comment Sentiment Analysis Dashboard

An advanced AI-powered analytics platform for analyzing YouTube comments with sentiment analysis, emotion detection, keyword extraction, and topic modeling.

## ✨ Features

### Core Features
- **YouTube Comment Extraction** - Automatically fetch comments from any YouTube video
- **Transformer-Based Sentiment Analysis** - Advanced NLP using DistilBERT model
- **Interactive Dashboard** - Beautiful, responsive analytics interface
- **Real-time Analysis** - Instant sentiment and emotion processing
- **CSV & Excel Export** - Download comprehensive reports

### Advanced Analytics
- **📊 Like Count Analysis** - Analyze engagement metrics and comment popularity
- **🔑 Keyword Extraction** - Identify top keywords and trends in comments
- **⭐ Top Positive/Negative Comments** - Find highest-rated comments by sentiment
- **📈 Trend Analysis** - Track sentiment patterns over time
- **💬 Engagement Metrics** - View likes, replies, and engagement distribution

### Advanced AI Features
- **😊 Emotion Detection** - Detect 10+ emotions (joy, anger, fear, surprise, etc.)
- **🌍 Multilingual Support** - Analyze comments in multiple languages (English, Hindi, Tamil, Spanish, etc.)
- **📚 Topic Modeling** - Automatically identify discussion topics using BERTopic
- **🔄 Real-time Monitoring** - Continuous comment analysis with auto-refresh capabilities

### Visualizations
- Sentiment distribution (pie charts, bar charts)
- Word clouds for text analysis
- Engagement trends over time
- Emotion distribution charts
- Keyword frequency analysis
- Topic clustering visualizations

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **NLP/AI** | Transformers, PyTorch, HuggingFace |
| **Data Processing** | Pandas, NumPy, Scikit-learn |
| **Visualization** | Plotly, Matplotlib, WordCloud |
| **API** | YouTube Data API v3 |
| **Deployment** | Streamlit Cloud, Docker, AWS |

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip or conda
- YouTube Data API key (get it [here](https://console.cloud.google.com/))

### Step 1: Clone Repository
```bash
git clone https://github.com/SHeBaJO/YouTube-Sentiment-Insight.git
cd YouTube-Sentiment-Insight
```

### Step 2: Create Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n youtube-sentiment python=3.10
conda activate youtube-sentiment
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup API Key

#### Option A: Using Streamlit Secrets
1. Create `.streamlit/secrets.toml`
```toml
YOUTUBE_API_KEY = "your_api_key_here"
```

#### Option B: Using Environment Variables
```bash
# Linux/Mac
export YOUTUBE_API_KEY="your_api_key_here"

# Windows
set YOUTUBE_API_KEY=your_api_key_here
```

### Step 5: Run Application
```bash
streamlit run app.py
```

Access the app at `http://localhost:8501`

---

## 🚀 Usage

### Basic Workflow

1. **Open Dashboard**
   - Navigate to the running Streamlit app

2. **Enter YouTube URL**
   - Paste a YouTube video link in the input field
   - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

3. **Configure Analysis**
   - Set maximum comments to analyze (10-500)
   - Toggle features (emotions, keywords, trends, topics)

4. **Start Analysis**
   - Click "🚀 Analyze Comments" button
   - Wait for analysis to complete

5. **Explore Results**
   - View KPI cards with summary statistics
   - Check visualizations and trends
   - Filter comments by sentiment
   - Export reports

### Export Options

- **CSV Export** - Simple comma-separated file
- **Excel Report** - Multi-sheet workbook with detailed analysis
- **Summary Report** - High-level metrics and statistics

---

## 📊 API Key Setup

### Getting YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials
5. Get your API key
6. Add to `.streamlit/secrets.toml` or environment variables

---

## 🔒 Security

### Best Practices
- ✅ Never commit API keys to GitHub
- ✅ Use `.gitignore` to exclude sensitive files
- ✅ Store secrets in environment variables or `.streamlit/secrets.toml`
- ✅ Use OAuth 2.0 for production deployments
- ✅ Rotate API keys regularly

### Files to Never Commit
```
.env
.streamlit/secrets.toml
credentials.json
*.key
```

---

## 📁 Project Structure

```
YouTube-Sentiment-Insight/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── .streamlit/
│   ├── config.toml                 # Streamlit configuration
│   └── secrets_template.toml       # Secrets template
├── src/
│   ├── __init__.py
│   ├── config.py                   # Configuration management
│   ├── utils/
│   │   ├── __init__.py
│   │   └── youtube_api.py          # YouTube API utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── sentiment.py            # Sentiment analysis
│   │   └── emotion.py              # Emotion detection
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── keywords.py             # Keyword extraction
│   │   ├── trends.py               # Trend analysis
│   │   └── topics.py               # Topic modeling
│   └── dashboard/
│       ├── __init__.py
│       ├── visualizations.py       # Visualization utilities
│       └── export.py               # Export functionality
├── README.md                       # Documentation
└── LICENSE                         # License file
```

---

## 🎯 Model Information

### Sentiment Analysis
- **Model**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Accuracy**: ~92% on sentiment classification
- **Languages**: English
- **Output**: Positive, Negative, Neutral + confidence score

### Emotion Detection
- **Model**: `j-hartmann/emotion-english-distilroberta-base`
- **Emotions**: Joy, Sadness, Anger, Fear, Surprise, Neutral
- **Languages**: English
- **Output**: Emotion label + confidence score

### Topic Modeling
- **Algorithm**: BERTopic (BERT-based topic modeling)
- **Method**: Transformer-based clustering
- **Output**: Topic labels, keywords, and assignments

### Multilingual Support (Optional)
- **Model**: `xlm-roberta-base`
- **Languages**: 100+ languages supported
- **Accuracy**: Varies by language

---

## 📈 Sample Dashboard Output

### KPI Section
```
📝 Total Comments: 234
😊 Positive: 156 (66.7%)
😠 Negative: 45 (19.2%)
😐 Neutral: 33 (14.1%)
⭐ Avg Confidence: 0.94
```

### Engagement Metrics
```
👍 Total Likes: 2,340
📊 Average Likes: 10.1
🔝 Max Likes: 567
💬 Average Replies: 2.3
```

---

## 🔧 Configuration

### Customize Analysis Parameters

Edit `src/config.py`:
```python
class Config:
    # Model Configuration
    SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
    EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
    
    # Analysis Settings
    MAX_COMMENTS_DEFAULT = 100
    CONFIDENCE_THRESHOLD = 0.5
    
    # Keyword Extraction
    TOP_KEYWORDS_COUNT = 10
```

---

## 🚀 Deployment

### Streamlit Cloud
```bash
# Push to GitHub, then deploy via Streamlit Cloud
# https://streamlit.io/cloud
```

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

### AWS/Heroku
Deploy using standard Python deployment processes with environment variables for API key.

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Code quality check
flake8 src/
black src/
```

---

## 📊 Performance Metrics

- **Comment Fetch Time**: 2-5 seconds (100 comments)
- **Sentiment Analysis**: 1-3 seconds (100 comments)
- **Emotion Detection**: 2-5 seconds (100 comments)
- **Keyword Extraction**: <1 second (100 comments)
- **Topic Modeling**: 5-15 seconds (100 comments)

---

## 🐛 Troubleshooting

### Issue: API Key Not Found
**Solution**: Ensure `.streamlit/secrets.toml` exists and contains `YOUTUBE_API_KEY`

### Issue: Model Download Failed
**Solution**: Check internet connection, wait for retry, or increase timeout

### Issue: Out of Memory
**Solution**: Reduce `max_comments` setting or increase system RAM

### Issue: No Comments Found
**Solution**: Video might have disabled comments or be private/deleted

---

## 📝 Example Use Cases

1. **Brand Monitoring** - Track customer sentiment on product videos
2. **Content Analysis** - Understand audience feedback on channel
3. **Marketing Insights** - Identify trending topics and concerns
4. **Research** - Analyze public opinion on YouTube videos
5. **Competitive Analysis** - Compare sentiment across competitor videos

---

## 🔮 Future Enhancements

- [ ] Channel-level sentiment analysis
- [ ] Cross-platform sentiment (Twitter, TikTok, Instagram)
- [ ] Advanced recommendation systems
- [ ] AI-generated audience insights
- [ ] Trend forecasting
- [ ] Business intelligence integrations
- [ ] Real-time alert system
- [ ] Sentiment prediction models

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/SHeBaJO/YouTube-Sentiment-Insight/issues)
- Submit a [Pull Request](https://github.com/SHeBaJO/YouTube-Sentiment-Insight/pulls)
- Check [Discussions](https://github.com/SHeBaJO/YouTube-Sentiment-Insight/discussions)

---

## 🎓 Credits

- **Streamlit** - Interactive dashboard framework
- **Hugging Face** - NLP models and transformers
- **YouTube Data API** - Comment extraction
- **BERTopic** - Topic modeling

---

## ⭐ Star History

If you find this project helpful, please star ⭐ the repository!

---

**Made with ❤️ for the Data Science and NLP Community**
