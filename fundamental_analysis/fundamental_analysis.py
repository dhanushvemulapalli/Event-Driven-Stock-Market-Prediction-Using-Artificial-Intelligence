#def fundamental_analysis(stock_code):
    #to be implemented
"""
    eg stock_code = 'AAPL'
    Retrieve fudamental indicator values for a stock.
    """
    # for your stock code, retrieve the following fundamental indicators
    #EPS = y_finace.get_earnings(stock_code)
    #FCF = y_finance.get_free_cash_flow(stock_code)
    #     
    # #Dividend Yield

    #check for conditons 

"""
    if eps = 50 :
        then return good ...
        #this is wrong, we need to compare the EPS with the industry average
    """

"""
        A More Strategic Approach:
        a combination of prioritizing core indicators and requiring balance:
                Core Indicators: ROE and FCF per Share.
                    Balance:
                        Require that at least one of ROE or FCF per share, passes the buy threshold.
                        Require that at least one of D/E trend or Earnings Growth, passes the buy threshold.
                        Require that PEG ratio change, passes the buy threshold.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import time
import random

def get_thresholds(sector):
    """
    Get sector-specific threshold values for fundamental indicators.

    Args:
        sector: The company's sector

    Returns:
        Dictionary of threshold values for each metric
    """
    # Base thresholds for general stocks
    base_thresholds = {
        'ROE': 0.15,             # 15% Return on Equity
        'D/E': 1.5,              # Maximum acceptable Debt-to-Equity ratio
        'FCF_PER_SHARE': 1.0,    # Minimum acceptable Free Cash Flow per share
        'EARNINGS_GROWTH': 0.10, # 10% earnings growth
        'PEG': 1.5               # Maximum acceptable Price/Earnings to Growth ratio
    }

    # Sector-specific threshold adjustments with realistic values
    sector_adjustments = {
        'Technology': {
            'ROE': 0.15,
            'D/E': 2.0,
            'FCF_PER_SHARE': 0.8,
            'EARNINGS_GROWTH': 0.08,
            'PEG': 2.2
        },
        'Healthcare': {
            'ROE': 0.12,
            'D/E': 1.5,
            'FCF_PER_SHARE': 0.6,
            'EARNINGS_GROWTH': 0.08,
            'PEG': 2.2
        },
        'Utilities': {
            'ROE': 0.08,
            'D/E': 2.8,
            'FCF_PER_SHARE': 0.3,
            'EARNINGS_GROWTH': 0.03,
            'PEG': 1.8
        },
        'Financial Services': {
            'ROE': 0.10,
            'D/E': 6.0,
            'FCF_PER_SHARE': 0.6,
            'EARNINGS_GROWTH': 0.06,
            'PEG': 1.8
        },
        'Consumer Cyclical': {
            'ROE': 0.12,
            'D/E': 2.5,
            'FCF_PER_SHARE': 0.6,
            'EARNINGS_GROWTH': 0.06,
            'PEG': 2.2
        },
        'Energy': {
            'ROE': 0.10,
            'D/E': 2.0,
            'FCF_PER_SHARE': 0.8,
            'EARNINGS_GROWTH': 0.05,
            'PEG': 1.8
        },
        'Consumer Defensive': {
            'ROE': 0.12,
            'D/E': 1.8,
            'FCF_PER_SHARE': 0.7,
            'EARNINGS_GROWTH': 0.05,
            'PEG': 2.0
        },
        'Industrials': {
            'ROE': 0.12,
            'D/E': 1.8,
            'FCF_PER_SHARE': 0.6,
            'EARNINGS_GROWTH': 0.07,
            'PEG': 1.8
        }
    }

    # Update base thresholds with sector-specific ones if available
    if sector in sector_adjustments:
        base_thresholds.update(sector_adjustments[sector])

    return base_thresholds

def fundamental_analysis(stock_code):
    """
    Performs fundamental analysis on a given stock using Yahoo Finance data.

    Args:
        stock_code (str): The ticker symbol for the stock (e.g., 'AAPL')

    Returns:
        str: Simple recommendation: "Buy", "Sell", or "Hold"
    """
    try:
        # Get stock data
        ticker = yf.Ticker(stock_code)
        info = ticker.info

        # Check if we have valid data
        if not info or len(info) < 5:
            return "Error"

        # Get financial statements
        try:
            balance_sheet = ticker.balance_sheet
            income_stmt = ticker.financials
            cash_flow = ticker.cashflow
        except:
            balance_sheet = pd.DataFrame()
            income_stmt = pd.DataFrame()
            cash_flow = pd.DataFrame()

        # Get the stock's sector
        sector = info.get('sector', 'General')

        # Get sector-specific thresholds
        thresholds = get_thresholds(sector)

        # Calculate metrics with fallbacks for missing data
        # Return on Equity (ROE)
        roe = info.get('returnOnEquity', 0)
        if roe == 0 and not balance_sheet.empty and not income_stmt.empty:
            equity_labels = ['Total Stockholder Equity', 'Stockholders Equity']
            income_labels = ['Net Income', 'Net Income Common Stockholders']

            try:
                total_equity = next((balance_sheet.loc[label].iloc[0]
                                  for label in equity_labels if label in balance_sheet.index), 1)
                net_income = next((income_stmt.loc[label].iloc[0]
                                for label in income_labels if label in income_stmt.index), 0)
                roe = net_income / total_equity if total_equity else 0
            except:
                pass

        # Debt-to-Equity Ratio
        de_ratio = info.get('debtToEquity', 0)
        if de_ratio == 0 and not balance_sheet.empty:
            try:
                equity_labels = ['Total Stockholder Equity', 'Stockholders Equity']
                debt_labels = ['Total Debt', 'Total Liab']

                total_equity = next((balance_sheet.loc[label].iloc[0]
                                  for label in equity_labels if label in balance_sheet.index), 1)
                total_debt = next((balance_sheet.loc[label].iloc[0]
                                for label in debt_labels if label in balance_sheet.index), 0)
                de_ratio = total_debt / total_equity if total_equity else 0
            except:
                pass

        # Convert debtToEquity from percentage to decimal if needed
        if de_ratio > 100:
            de_ratio = de_ratio / 100

        # Free Cash Flow per Share
        fcf_per_share = 0
        try:
            if 'freeCashflow' in info and 'sharesOutstanding' in info and info.get('sharesOutstanding', 0) > 0:
                fcf_per_share = info.get('freeCashflow', 0) / info.get('sharesOutstanding', 1)
            elif not cash_flow.empty:
                if 'Free Cash Flow' in cash_flow.index:
                    fcf = cash_flow.loc['Free Cash Flow'].iloc[0]
                elif all(label in cash_flow.index for label in ['Operating Cash Flow', 'Capital Expenditure']):
                    fcf = cash_flow.loc['Operating Cash Flow'].iloc[0] - cash_flow.loc['Capital Expenditure'].iloc[0]
                else:
                    fcf = 0

                shares = info.get('sharesOutstanding', 1)
                fcf_per_share = fcf / shares if shares else 0
        except:
            pass

        # PEG Ratio
        peg_ratio = info.get('pegRatio', 3.0)
        if peg_ratio == 0 or peg_ratio > 10:
            peg_ratio = 3.0

        # Earnings Growth
        earnings_growth = info.get('earningsGrowth', 0)
        if isinstance(earnings_growth, (int, float)) and earnings_growth > 2:
            earnings_growth = earnings_growth / 100

        # Calculate score
        score = 0

        # ROE Evaluation (0-20 points)
        if roe >= thresholds['ROE']:
            score += 20
        elif roe >= thresholds['ROE'] * 0.7:
            score += 14
        elif roe >= thresholds['ROE'] * 0.5:
            score += 7

        # FCF per Share Evaluation (0-15 points)
        if fcf_per_share >= thresholds['FCF_PER_SHARE']:
            score += 15
        elif fcf_per_share >= thresholds['FCF_PER_SHARE'] * 0.7:
            score += 10
        elif fcf_per_share >= thresholds['FCF_PER_SHARE'] * 0.4:
            score += 5

        # D/E Ratio Evaluation (0-20 points)
        if de_ratio <= thresholds['D/E']:
            score += 20
        elif de_ratio <= thresholds['D/E'] * 1.3:
            score += 14
        elif de_ratio <= thresholds['D/E'] * 1.7:
            score += 7

        # Earnings Growth Evaluation (0-20 points)
        if earnings_growth >= thresholds['EARNINGS_GROWTH']:
            score += 20
        elif earnings_growth >= thresholds['EARNINGS_GROWTH'] * 0.7:
            score += 14
        elif earnings_growth >= thresholds['EARNINGS_GROWTH'] * 0.4:
            score += 7

        # PEG Ratio Evaluation (0-25 points)
        if peg_ratio <= thresholds['PEG']:
            score += 25
        elif peg_ratio <= thresholds['PEG'] * 1.3:
            score += 17
        elif peg_ratio <= thresholds['PEG'] * 1.7:
            score += 8

        # Generate simplified recommendation
        if score >= 75:
            return 1
        elif score >= 55:
            return 0.5
        elif score >= 35:
            return 0
        elif score >= 20:
            return -0.5
        else:
            return -1

    except Exception as e:
        return "Error"