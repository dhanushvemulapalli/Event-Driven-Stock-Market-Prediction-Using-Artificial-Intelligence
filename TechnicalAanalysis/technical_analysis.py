import yfinance as yf
import pandas as pd
import numpy as np

def technical_analysis(stock_code):
    """
    Performs technical analysis on a given stock using Yahoo Finance data.

    Args:
        stock_code (str): The ticker symbol for the stock (e.g., 'AAPL')

    Returns:
        str: Recommendation based on technical indicators: "Buy", "Sell", or "Hold"
    """
    try:
        # Fetch historical data (last 100 days for a 50-day SMA & Bollinger Bands)
        ticker = yf.Ticker(stock_code)
        hist = ticker.history(period="100d")

        if hist.empty:
            return "Error: No data available"

        close_prices = hist['Close']

        # Compute SMA (50-day)
        sma50 = close_prices.rolling(window=50).mean().iloc[-1]

        # Compute EMA (50-day)
        ema50 = close_prices.ewm(span=50, adjust=False).mean().iloc[-1]

        # Compute EMA (21-day) for MACD
        ema21 = close_prices.ewm(span=21, adjust=False).mean().iloc[-1]

        # MACD Calculation
        macd = ema21 - ema50
        signal_line = macd * 0.9 + macd * 0.1  # Approximate 9-day signal line

        # RSI Calculation (21-day)
        delta = close_prices.diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        avg_gain = pd.Series(gain).rolling(window=21).mean().iloc[-1]
        avg_loss = pd.Series(loss).rolling(window=21).mean().iloc[-1]

        rs = avg_gain / avg_loss if avg_loss != 0 else np.inf
        rsi = 100 - (100 / (1 + rs))

        # Bollinger Bands (50-day)
        rolling_std = close_prices.rolling(window=50).std().iloc[-1]
        upper_band = sma50 + (2 * rolling_std)
        lower_band = sma50 - (2 * rolling_std)

        # Latest Price
        latest_price = close_prices.iloc[-1]

        # Trading Signal Decision
        score = 0

        # Trend Confirmation (SMA)
        if latest_price > sma50:
            score += 20  # Uptrend
        elif latest_price < sma50:
            score -= 20  # Downtrend

        # Momentum Indicators (MACD, RSI)
        if macd > signal_line:
            score += 20  # Bullish momentum
        else:
            score -= 20  # Bearish momentum

        if rsi > 75:
            score -= 15  # Overbought
        elif rsi < 25:
            score += 15  # Oversold

        # Volatility Breakout Detection (Bollinger Bands)
        if latest_price <= lower_band and rsi > 20:
            score += 15  # Reversal Signal
        if latest_price >= upper_band and rsi < 80:
            score -= 15  # Possible Drop

        # Generate Recommendation
        print(score)
        if score >= -10:
            return 1
        elif score <= -40:
            return 1
        else:
            return 0

    except Exception as e:
        return f"Error: {str(e)}"
