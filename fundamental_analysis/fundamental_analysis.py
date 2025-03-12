def fundamental_analysis(stock_code):
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