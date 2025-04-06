import pickle
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer

# ========== Loaders ==========

def load_trained_model(model_path):
    with open(model_path, 'rb') as file:
        return pickle.load(file)

def load_polynomial_features(poly_path):
    with open(poly_path, 'rb') as file:
        return pickle.load(file)

def load_scaler(scaler_path):
    with open(scaler_path, 'rb') as file:
        return pickle.load(file)

# ========== Data Fetching ==========

def fetch_stock_data(symbol, period="3mo", interval="1d"):
    df = yf.download(symbol, period=period, interval=interval)
    return df.dropna()

# ========== Feature Engineering ==========

import pandas as pd

def transform_stock_data(df, window_size=50):
    # Ensure required columns exist
    if 'Close' not in df.columns or 'Volume' not in df.columns:
        raise ValueError("Input DataFrame must contain 'Close' and 'Volume' columns.")
    
    transformed = []
    for i in range(len(df) - window_size + 1):
        window = df.iloc[i:i+window_size]
        # Correctly create a row with Close and Volume features
        row = window[['Close', 'Volume']].values.flatten()  # Combine Close and Volume
        transformed.append(row)

    # Correctly generate column names dynamically
    columns = []
    for i in range(1, window_size + 1):
        columns.append(f"close{i}")
        columns.append(f"vol{i}")

    return pd.DataFrame(transformed, columns=columns)  # Return DataFrame with proper features
# ========== Technical Indicators ==========

def calculate_ATR(df, period=14):
    high, low, close = df['High'], df['Low'], df['Close']
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()

def get_support_resistance(df, window=20):
    support = df['Close'].rolling(window).min()
    resistance = df['Close'].rolling(window).max()
    return support, resistance

def calculate_trade_levels(row, multiplier=1.5):
    sl = row['Support'] - multiplier * row['ATR']
    fib_target = row['FibExtension']
    res_target = row['Resistance']
    pred_target = row['PredictedMax']
    final_target = min(fib_target, res_target, pred_target)
    return pd.Series([sl, final_target], index=['StopLoss', 'Target'])

# ========== Signal Generation ==========

def generate_signal_from_sequence(prices, threshold=0.005):
    current = prices[0]
    future_mean = np.mean(prices[1:])
    change = (future_mean - current) / current
    if change > threshold:
        return 1  # Buy
    elif change < -threshold:
        return -1  # Sell
    else:
        return 0  # Hold

# ========== Forecast Pipeline ==========

def forecast_stock(stock_code):
    # Load assets
    model = load_trained_model(r'C:\Users\dhanu\OneDrive\Desktop\IDP\Event-Driven-Stock-Market-Prediction-Using-Artificial-Intelligence\forecasting\trained_polynomial_regression_model.pkl')
    poly = load_polynomial_features(r'C:\Users\dhanu\OneDrive\Desktop\IDP\Event-Driven-Stock-Market-Prediction-Using-Artificial-Intelligence\forecasting\polynomial_features.pkl')
    # scaler = load_scaler('min_max_scaler.pkl')

    # Load stock data
    df = fetch_stock_data(stock_code, period="6mo", interval="1d")
    if len(df) < 60:
        raise ValueError("Not enough data to generate input features (need >60 days).")

    # Create ML input
    features_df = transform_stock_data(df[-60:].copy(), window_size=50)
    # scaled_features = pd.DataFrame(scaler.transform(features_df), columns=features_df.columns)
    X = features_df[[f'close{i}' for i in range(1, 51)] + [f'vol{i}' for i in range(1, 51)]]
    # Impute NaN values using SimpleImputer 
    # Create an imputer object with strategy 'mean'
    imputer = SimpleImputer(strategy='mean')  
    # Fit the imputer on your data and transform it
    X = imputer.fit_transform(X)
    X_poly = poly.transform(X)

    # Predict close50 to close58
    y_pred = model.predict(X_poly)
    prediction_df = pd.DataFrame(y_pred, columns=[f'close{i}' for i in range(51, 59)])
    prediction_df['PredictedMax'] = prediction_df[[f'close{i}' for i in range(51, 59)]].max(axis=1)
    signal = generate_signal_from_sequence(prediction_df.iloc[0].values)

    import yfinance as yf
    hist = yf.download(stock_code, period="1mo", interval="1d")
    hist.reset_index(inplace=True)

    # Signal
    hist['ATR'] = calculate_ATR(hist)
    hist['Support'] = hist['Close'].rolling(20).min()
    hist['Resistance'] = hist['Close'].rolling(20).max()

    # Ensure 'Support' is a Series before using it in the calculation
    fib_extension= hist['Close'].values + 1.618 * (hist['Close'].values - hist['Support'].fillna(hist['Close'].iloc[-1]).values)
    
    latest = hist.iloc[-1]
    latest_fibex = fib_extension[-1]
    predicted_max = prediction_df.loc[0, 'PredictedMax']

    stoploss = latest['Support'] - 1.5 * latest['ATR']
    target = min(latest_fibex[-1], latest['Resistance'].values[0], predicted_max)

    return signal,round(stoploss[-1],2),target

# Example usage:
# result = forecast_stock("AAPL")
