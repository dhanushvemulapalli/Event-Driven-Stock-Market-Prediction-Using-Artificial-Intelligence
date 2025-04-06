"""
# My first app
Here's our first attempt at using data to create a table:
"""
import Sentiment_analysis.SentAnalysis as SentAna
import forecasting.idp as forecast
import TechnicalAanalysis.technical_analysis as TechAna
import fundamental_analysis.fundamental_analysis as FundAna

stock_code = "TSLA"

SentAna = SentAna.SentAna(stock_code)
forecast = forecast.forecast_stock(stock_code)
TechAna = TechAna.technical_analysis(stock_code)
FundAna = FundAna.fundamental_analysis(stock_code)

print("Sentiment Analysis: ", SentAna)
print("Forecast Analysis: ", forecast)
print("Technical Analysis: ", TechAna)
print("Fundamental Analysis: ", FundAna)

w_sen = 1
w_for = 1
w_tec = 1
w_fun = 1

final_answer = (w_sen * SentAna + w_for * forecast[0] + w_tec * TechAna + w_fun* FundAna)/(w_fun +w_for+w_tec+w_sen )

#### !!! TEST !!!
# import streamlit as st
# import pandas as pd
# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))
