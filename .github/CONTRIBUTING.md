# Contributing to YouTube Sentiment Insight Bot

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs
1. Check existing [Issues](https://github.com/SHeBaJO/YouTube-Sentiment-Insight/issues)
2. Provide detailed description with:
   - Python version
   - OS and environment
   - Steps to reproduce
   - Error messages/logs
   - Expected vs actual behavior

### Suggesting Features
1. Describe the feature clearly
2. Explain the use case and benefits
3. Provide examples if possible
4. Discuss potential implementation approach

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes with clear commit messages
4. Write/update tests as needed
5. Ensure code follows PEP 8 style
6. Submit PR with description of changes

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/YouTube-Sentiment-Insight.git
cd YouTube-Sentiment-Insight

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dev dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Copy environment template
cp .env.example .env
```

## Code Standards

### Style
- Follow PEP 8
- Use 4 spaces for indentation
- Max line length: 100 characters
- Use type hints where applicable

### Formatting
```bash
# Format code
black .

# Check style
flake8 .
```

### Documentation
- Add docstrings to functions and classes
- Update README for new features
- Include examples for complex features
- Document configuration changes

## Testing

```bash
# Run tests
pytest tests/

# Check coverage
pytest --cov=src tests/
```

## Areas for Contribution

### High Priority
- [ ] Persistent database (SQLite/PostgreSQL)
- [ ] Multilingual support
- [ ] Real-time monitoring
- [ ] Web dashboard

### Medium Priority
- [ ] Advanced visualizations
- [ ] Performance optimization
- [ ] More NLP models
- [ ] API endpoint

### Low Priority
- [ ] UI improvements
- [ ] Documentation
- [ ] Examples
- [ ] Tutorials

## Commit Message Guidelines

Format: `<type>: <subject>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Test additions/changes

Example:
```
feat: add multilingual sentiment analysis

- Implement XLM-RoBERTa model support
- Add language detection
- Support 10 new languages
```

## Questions?

- Open an Issue for discussions
- Check existing documentation
- Review related Issues/PRs

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Report inappropriate behavior

---

Thank you for contributing! 🎉
