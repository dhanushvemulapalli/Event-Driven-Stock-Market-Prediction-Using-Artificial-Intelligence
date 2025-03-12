import nltk
nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize VADER
def VaderAnalysis(news):
    """
    Perform sentiment analysis on a news article using VADER.

    Args:
        news (str): News article to analyze.

    Returns:
        dict: Dictionary with sentiment scores ('neg', 'neu', 'pos', 'compound')
    """
    sia = SentimentIntensityAnalyzer()

    # Custom finance-related sentiment words
    finance_lexicon = {
        "bullish": 3.0,
        "bearish": -3.0,
        "profit": 2.5,
        "loss": -2.5,
        "growth": 2.0,
        "recession": -3.0,
        "default": -2.0,
        "volatile": -1.5,
        "plunge": -3.0,
        "selloff": -2.5,
        "collapse": -3.0,
        "crash": -3.5,
        "downtrend": -2.5,
        "pullback": -2.0,
        "bear market": -3.0,
        "overvalued": -1.5,
        "decline": -2.0,
        "correction": -1.5,
        "downgrade": -2.0,
        "default risk": -3.0,
        "bankruptcy": -3.5,
        "layoffs": -2.5,
        "missed earnings": -2.5,
        "deficit": -2.5,
        "liquidation": -3.0

    }

    # Update VADER's lexicon
    sia.lexicon.update(finance_lexicon)
    scores = sia.polarity_scores(text)
    return scores

"""
# Test

text = "HDFC Bank among top 8 trading ideas for 20 February 2025."

scores = VaderAnalysis(text)    
print(scores)

"""
