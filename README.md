# Shelf Genius: Your AI-Powered Book Recommendation Companion



[![GitHub Actions Status](https://img.shields.io/github/actions/workflow/status/PatrickKalkman/shelf-genius/ci.yml?branch=master)](https://github.com/PatrickKalkman/shelf-genius/actions)
[![GitHub stars](https://img.shields.io/github/stars/PatrickKalkman/shelf-genius)](https://github.com/PatrickKalkman/shelf-genius/stargazers)
[![GitHub contributors](https://img.shields.io/github/contributors/PatrickKalkman/shelf-genius)](https://github.com/PatrickKalkman/shelf-genius/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/PatrickKalkman/shelf-genius)](https://github.com/PatrickKalkman/shelf-genius)
[![open issues](https://img.shields.io/github/issues/PatrickKalkman/shelf-genius)](https://github.com/PatrickKalkman/shelf-genius/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)

Ever stared at your bookshelf, wishing it could tell you what to read next? Shelf Genius transforms a simple photo of your bookshelf into personalized reading recommendations using the power of AI. By analyzing your current collection and understanding the subtle connections between books, it suggests your next perfect read – no more endless scrolling through generic recommendations!

## ✨ Key Features

- **Smart Book Detection**: Uses advanced AI vision to identify books from a simple photo of your bookshelf
- **Deep Understanding**: Goes beyond just titles, analyzing themes, writing styles, and connections between books
- **Personalized Magic**: Creates thoughtful, individual recommendations based on your unique reading journey
- **Google Books Integration**: Enriches recommendations with detailed book information and metadata
- **Local AI Support**: Option to run book recognition and recommendations locally for privacy and cost savings
- **Clean Output**: Delivers recommendations in clear, readable formats with detailed explanations

## 🚀 Getting Started

Shelf Genius uses UV for seamless Python package management and execution. Here's how to get up and running in minutes.

### Prerequisites

- Python 3.10 or higher
- Git
- OpenAI API key (for GPT-4 Vision)

### Installation

1. **Install UV** - Your friendly package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone Shelf Genius**:
```bash
git clone https://github.com/YourUsername/shelf-genius
cd shelf-genius
```

3. **Set up your API key**:
```bash
echo "OPENAI_API_KEY=your-key-goes-here" > .env
```

### Running Shelf Genius

Got a photo of your bookshelf? Let's get some recommendations! Use UV's run command:

```bash
uv run python ./src/shelf_genius/workflow.py --image path/to/your/photo.jpg
```

Want to see what's happening under the hood? Add the verbose flag:

```bash
uv run python ./src/shelf_genius/workflow.py --image path/to/your/photo.jpg --verbose
```

## 📚 How It Works

Shelf Genius uses a four-stage process to turn your bookshelf photo into personalized recommendations:

1. **Image Processing**: Optimizes your photo for AI analysis
2. **Book Recognition**: Uses GPT-4 Vision to identify books in your collection
3. **Metadata Enhancement**: Enriches book data using the Google Books API
4. **Smart Recommendations**: Analyzes patterns and connections to suggest your next read

## 🎯 Example Output

Here's what you can expect from Shelf Genius:

```json
{
  "recommendation": {
    "title": "The Design of Everyday Things",
    "author": "Don Norman",
    "reasoning": "Based on your collection's focus on both technical topics and human-centered design, this book bridges the gap between technology and usability - a perfect next read for you!"
  }
}
```

## 🤝 Contributing

Got ideas for making Shelf Genius even better? I'd love your help! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Check out our [Contributing Guide](CONTRIBUTING.md) for more details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Shelf Genius stands on the shoulders of giants:

- OpenAI's GPT-4 Vision for book recognition
- Google Books API for rich metadata
- UV for elegant package management
- The incredible open-source community

## 🌟 What's Next?

Shelf Genius is growing! Coming soon:
- Local AI support for offline book recognition
- Enhanced recommendation algorithms
- Multi-language support
- Web interface for easier use

Want to help shape the future of Shelf Genius? Star the repo, open an issue, or submit a PR. Let's make book discovery magical together! 🚀
