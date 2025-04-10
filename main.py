"""
# My first app
Here's our first attempt at using data to create a table:
"""
import os
import alpaca_trade_api as tradeapi

ALPACA_API_KEY = "PK71KD6R1CVL2QCK3NPC"  # Set this in your environment or replace with string
ALPACA_SECRET_KEY = "VDTK860mEcqSQYzXlzkeZDDW2RTb7L1tftMzb42F"
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"  # For live trading, change to live URL

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, api_version='v3')

import Sentiment_analysis.SentAnalysis as SentAna
import forecasting.idp as forecast
import TechnicalAanalysis.technical_analysis as TechAna
import fundamental_analysis.fundamental_analysis as FundAna

import Sentiment_analysis.SentAnalysis as SentAna
import forecasting.idp as forecast
import TechnicalAanalysis.technical_analysis as TechAna
import fundamental_analysis.fundamental_analysis as FundAna
import alpaca_trade_api as tradeapi
import os
import math

# Set up Alpaca credentials
# ALPACA_API_KEY = "ALPACA_API_KEY"
# ALPACA_SECRET_KEY = "ALPACA_SECRET_KEY"
# ALPACA_BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, api_version='v2')

def place_order(symbol, side, qty, stop_price):
    try:
        # Place market order
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        print(f"{side.upper()} order placed for {symbol}")

        # Only set stop-loss if it's a BUY
        if side == "buy":
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side="sell",
                type="stop",
                stop_price=stop_price,
                time_in_force='gtc'
            )
            print(f"STOP-LOSS set at {stop_price} for {symbol}")

    except Exception as e:
        print(f"Failed to place {side} order for {symbol}: {e}")
def get_current_positions():
    try:
        positions = api.list_positions()
        owned_symbols = {position.symbol: float(position.qty) for position in positions}
        return owned_symbols
    except Exception as e:
        print(f"Error fetching current positions: {e}")
        return {}

def Analyse_Stock(stock_code, portfolio):
    sentiment_analysis = SentAna.SentAna(stock_code)
    forecast_result = forecast.forecast_stock(stock_code)
    technical_analysis = TechAna.technical_analysis(stock_code)
    fundamental_analysis = FundAna.fundamental_analysis(stock_code)

    print("\n--- Analysis ---")
    print("Sentiment Analysis: ", sentiment_analysis)
    print("Forecast Analysis: ", forecast_result)
    print("Technical Analysis: ", technical_analysis)
    print("Fundamental Analysis: ", fundamental_analysis)

    final_answer = (40 * sentiment_analysis + 10 * forecast_result[0] +
                    35 * technical_analysis + 20 * fundamental_analysis) / 100
    print("Final Decision Score:", final_answer)

    action = "hold"
    if final_answer > 0:
        action = "buy"
    elif final_answer < -0.1 and stock_code in portfolio:
        action = "sell"

    print(f"Action: {action.upper()}")

    if action in ["buy", "sell"]:
        side = action
        stop_loss = forecast_result[1]
        target = forecast_result[2]
        place_order(stock_code, side, qty=1, stop_price=stop_loss)
        stop_loss = float(forecast_result[1])

        if stop_loss <= 0 or not math.isfinite(stop_loss):
            print(f"Invalid stop-loss value for {stock_code}. Skipping {action} order.")
            return

        place_order(stock_code, side=action, qty=1, stop_price=stop_loss)


    print("-------------------\n")
# nasdaq_stock_codes = [
#     "AAPL", "MSFT", "AMZN", "GOOG", "TSLA", "NVDA", "META", "AVGO", "PEP", "CSCO",
#     "ADBE", "COST", "CMCSA", "TXN", "NFLX", "QCOM", "INTC", "AMD", "CRM", "PYPL",
#     "AMGN", "GILD", "ISRG", "MDLZ", "BKNG", "ADI", "MU", "SBUX", "INTU", "ADP",
#     "FISV", "CHTR", "MRNA", "REGN", "LRCX", "VRTX", "ILMN", "DXCM", "ADI",
#     "MELI", "ZM", "DDOG", "SNOW", "DOCU", "OKTA", "CRWD", "TWLO", "PLTR", "ROKU",
#     "MDB", "NET", "CFLT", "BYND", "PINS", "APPS", "SMCI", "FIVN", "TEAM", "WDAY",
#     "COUP", "ZS", "CDAY", "VEEV", "TTD", "DDOG", "HUBS", "DOCS", "CLDR", "WORK",
#     "MTCH", "TWTR", "SQ", "SHOP", "DASH", "U", "UBER", "LYFT", "COIN", "HOOD",
#     "NFLX", "DIS", "WBD", "PARA", "AMC", "FUBO", "RNG", "EA", "ATVI", "TTWO",
#     "MS", "GS", "JPM", "BAC", "C", "WFC", "USB", "PNC", "SCHW", "AXP",
#     "V", "MA", "PYPL", "AEP", "NEE", "DUK", "SO", "EXC", "D", "ED",
#     "XOM", "CVX", "COP", "EOG", "OXY", "MPC", "PXD", "SLB", "HAL", "VLO",
#     "TSM", "ASML", "NVDA", "INTC", "AMD", "QCOM", "MU", "STM", "ADI", "MRVL",
#     "CRM", "ORCL", "SAP", "IBM", "ADBE", "INTU", "NOW", "TEAM", "WDAY", "ZEN"
# ]

nasdaq_stock_codes = ["AAPL", "MSFT", "AMZN", "GOOG", "TSLA", "NVDA", "META", "AVGO", "PEP", "CSCO","PYPL","ORCL", "SAP", "IBM", "ADBE", "INTU", "NOW", "TEAM", "WDAY", "ZEN"]
portfolio = get_current_positions()

for stock in nasdaq_stock_codes:
    print("================================================================")
    print(f"Analysing stock: {stock}")
    try:
        Analyse_Stock(stock, portfolio)
        print(f"Analysis complete for {stock}\n")
    except Exception as e:
        print(f"Error analysing {stock}: {e}\n")
    print("=================================================================")

