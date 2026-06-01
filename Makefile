# Makefile for development tasks

.PHONY: help install dev test lint format run deploy clean docker

help:
	@echo "YouTube Sentiment Analysis Dashboard - Development Tasks"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Setup development environment"
	@echo "  make run        - Run the Streamlit app"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Check code style"
	@echo "  make format     - Format code"
	@echo "  make clean      - Remove cache files"
	@echo "  make docker     - Build Docker image"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install pytest black flake8 pytest-cov

run:
	streamlit run app.py

test:
	pytest tests/ -v --cov=src

lint:
	flake8 src/ app.py

format:
	black src/ app.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/

docker:
	docker build -t youtube-sentiment-dashboard .
	docker run -p 8501:8501 youtube-sentiment-dashboard

docker-run:
	docker run -p 8501:8501 -e YOUTUBE_API_KEY=${YOUTUBE_API_KEY} youtube-sentiment-dashboard
