import yfinance as yf
import pandas as pd
import os
from collections import OrderedDict

ROOTDIR = os.path.abspath(os.curdir)
companies = ['SPY', 'MSFT', 'BTC-USD']

def get_historical_data(ticker, period):
    ticker = 'AAPL'
    file_to_save = os.path.join(ROOTDIR, 'market_data', ticker + '.csv')
    data = yf.download(tickers = ticker, period = '10y', interval = "1d", ignore_tz = True, prepost = False)
    print(data)
    data.to_csv(file_to_save)

def get_watchlist_prices(companies):
    stock_prices = {}
    tickers = yf.Tickers(companies)
    for company in companies:
        try:
            price = round(tickers.tickers[company].fast_info['lastPrice'], 2)
            if not pd.isna(price):
                stock_prices[company] = price
        except:
            pass
    return OrderedDict(sorted(stock_prices.items()))

def get_stocks(companies):
    tickers = yf.Tickers(companies)
    return tickers

def get_current_prices(companies, stock_responses):
    stock_prices = {}
    for company in companies:
        try:
            price = round(stock_responses.tickers[company].fast_info['lastPrice'], 2)
            if not pd.isna(price):
                stock_prices[company] = price
        except:
            pass
    return stock_prices

def save_historical_data(company):
    try:
        file_to_save = os.path.join(ROOTDIR, 'market_data', company + '.csv')
        data = yf.download(tickers = company, period = '1y', interval = "1d", ignore_tz = True, prepost = False)
        data.to_csv(file_to_save)
        return data
    except Exception as e:
        print(e)

if __name__ == "__main__":
    print(get_stocks(companies))
