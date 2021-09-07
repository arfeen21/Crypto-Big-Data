import yfinance
from datetime import datetime

def get():
    '''
    Returns a cleaned dataframe of hourly $TSLA data starting from November 1st 2020 until today.

    Column names of the dataframe:
        - Date
        - HourlyPrice
    '''

    #we start our analysis on data published after the 1st of November 2020.
    startDate = "2020-11-01"

    #we use the string format method of datetime module to properly format today's date for the API
    endDate = datetime.today().strftime("%Y-%m-%d")

    tsla = yfinance.Ticker("TSLA")

    #we then use the yfinance wrapper to get hourly $TSLA data from November 1st until now
    stockData = tsla.history(start=startDate, end=endDate, interval="1h")

    #removing unnecessary columns (axis = 1 means we want to drop columns instead of rows)
    stockData = stockData.drop(['High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'], axis=1)

    #calling reset_index ensures we have the Date as a separate column instead of it being the index to a row
    stockData.reset_index(level=0, inplace=True)

    stockData.rename({"Open": "HourlyPrice"}, inplace=True, axis=1)

    return stockData
