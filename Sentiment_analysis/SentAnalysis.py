import nltk
nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize VADER
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
"bullish": 0.83,
"bearish": -0.95,
"profitloss": -1.00,
"default": -0.85,
"volatile": -0.54,
"plunge": -0.99,
"selloff": -0.89,
"collapse": -1.00,
"crash": -0.99,
"downtrend": -0.78,
"pullback": -0.13,
"overvalued": -0.98,
"decline": -0.91,
"correction": -0.82,
"downgrade": -0.98,
"bankruptcy": -0.95,
"layoffs": -0.99,
"deficit": -0.65,
"liquidation": -0.94

}

# Update VADER's lexicon
sia.lexicon.update(finance_lexicon)


"""
# Test

text = "HDFC Bank among top 8 trading ideas for 20 February 2025."

scores = VaderAnalysis(text)    
print(scores)

"""

def get_sentiment(text):
  scores = sia.polarity_scores(text)
  return scores['compound']

import requests
import xmltodict
from yahoo_fin import news as yf_news


def get_stock_news(stock_code):
    news_data = {}

    # Yahoo Finance News
    try:
        yahoo_news = yf_news.get_yf_rss(stock_code)
        news_data["Yahoo Finance"] = [
            {"title": item["title"], "link": item["link"], "Score" : get_sentiment(item["title"])}
            for item in yahoo_news
        ]
    except Exception as e:
        news_data["Yahoo Finance"] = f"Error fetching Yahoo Finance news: {e}"

    # Reddit Stock News (RSS)
    reddit_url = f"https://www.reddit.com/r/{stock_code}/.rss"
    try:
        response = requests.get(reddit_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            reddit_feed = xmltodict.parse(response.content)
            entries = reddit_feed["feed"].get("entry", [])
            if isinstance(entries, dict):  # If only one entry exists
                entries = [entries]
            news_data["Reddit"] = [
                {"title": item["title"], "link": item["link"]["@href"], "Score" : get_sentiment(item["title"])}
                for item in entries
            ]
        else:
            news_data["Reddit"] = f"Failed to fetch data: {response.status_code}"
    except Exception as e:
        news_data["Reddit"] = f"Error fetching Reddit news: {e}"

    return news_data


def SentAna(stock_symbol):
    news = get_stock_news(stock_symbol)
    scores = []  # Store sentiment scores

    for source, articles in news.items():
        # print(f"\n{source} News:")
        if isinstance(articles, list):
            for article in articles[:5]:  # Show only top 5
                # print(f"- {article['title']} (Score: {article['Score']})\n  Link: {article['link']}")
                scores.append(article["Score"])  # Collect sentiment scores
        # else:
        #     print(articles)

    # Calculate average sentiment score
    avg_sentiment = sum(scores) / len(scores)
    # if scores:
        
    #     # print(f"\nAverage Sentiment Score: {avg_sentiment:.3f}")

    #     # Decide Buy, Sell, or Neutral
    #     if avg_sentiment >= 0.5:
    #         # print("\n🚀 **Signal: BUY** 🚀 (Positive sentiment)")
    #         return 1 
    #     elif avg_sentiment <= -0.5:
    #         # print("\n⚠️ **Signal: SELL** ⚠️ (Negative sentiment)")
    #         return -1
    #     else:
    #         # print("\n🔍 **Signal: NEUTRAL** 🔍 (Mixed sentiment)")
    #         return 0
    # else:
    #     print("\n❌ No news articles found. Cannot determine sentiment.")


    return avg_sentiment


# ans = SentAna("TSLA")
# print(ans)