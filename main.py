"""
# My first app
Here's our first attempt at using data to create a table:
"""
import Sentiment_analysis.SentAnalysis as SentAna
import forecasting.idp as forecast
import TechnicalAanalysis.technical_analysis as TechAna
import fundamental_analysis.fundamental_analysis as FundAna

def Analyse_Stock(stock_code):
    sentiment_analysis = SentAna.SentAna(stock_code)
    forecast_result = forecast.forecast_stock(stock_code)
    technical_analysis = TechAna.technical_analysis(stock_code)
    fundamental_analysis = FundAna.fundamental_analysis(stock_code)

    print()
    print()

    print("Sentiment Analysis: ", sentiment_analysis)
    print("Forecast Analysis: ", forecast_result)
    print("Technical Analysis: ", technical_analysis)
    print("Fundamental Analysis: ", fundamental_analysis)

    print()

    final_answer = (45*sentiment_analysis + 10* forecast_result[0] + 25*technical_analysis + 20*fundamental_analysis) / 100
    print("Final Decision:", final_answer)
    print()


Analyse_Stock("AAPL")
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

for stock in nasdaq_stock_codes:
    print("================================================================")
    print(f"Analysing stock: {stock}")
    try:
        Analyse_Stock(stock)
        print(f"Analysis complete for {stock}\n")
    except Exception as e:
        print(f"Error analysing {stock}: {e}\n")
    print("=================================================================")


