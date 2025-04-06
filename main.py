"""
# My first app
Here's our first attempt at using data to create a table:
"""
import Sentiment_analysis.SentAnalysis as SentAna
# import forecasting.idp as forecast
# import TechnicalAanalysis as TechAna
import fundamental_analysis.fundamental_analysis as FundAna

stock_code = "META"

SentAna = SentAna.SentAna(stock_code)
# forecast = forecast.forecast(stock_code)
# TechAna = TechAna.TechAna(stock_code)
FundAna = FundAna.fundamental_analysis(stock_code)

print("Sentiment Analysis: ", SentAna)
# print("Forecast Analysis: ", forecast)
# print("Technical Analysis: ", TechAna)
print("Fundamental Analysis: ", FundAna)

#### !!! TEST !!!
# import streamlit as st
# import pandas as pd
# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))
