# Event-Driven Stock Market Prediction Using Artificial Intelligence

This project implements a comprehensive stock market prediction system that combines multiple analysis techniques to provide accurate stock price predictions.

## Features

- **Sentiment Analysis**: Analyzes market sentiment from news and social media
- **Technical Analysis**: Uses historical price patterns and technical indicators
- **Fundamental Analysis**: Evaluates company financials and market position
- **Forecasting**: Implements time series forecasting models
- **Weighted Prediction**: Combines all analyses with configurable weights

## Project Structure

```
.
├── main.py                 # Main application entry point
├── Sentiment_analysis/     # Sentiment analysis module
├── forecasting/           # Time series forecasting module
├── TechnicalAanalysis/    # Technical analysis module
├── fundamental_analysis/  # Fundamental analysis module
├── src/                  # Source code utilities
└── Docs/                 # Documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Event-Driven-Stock-Market-Prediction-Using-Artificial-Intelligence.git
cd Event-Driven-Stock-Market-Prediction-Using-Artificial-Intelligence
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script with a stock symbol:
```bash
python main.py
```

## Configuration

The system uses weighted analysis where you can adjust the importance of each analysis type:
- w_sen: Sentiment analysis weight
- w_for: Forecasting weight
- w_tec: Technical analysis weight
- w_fun: Fundamental analysis weight

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
