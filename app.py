from flask import Flask, render_template, request, redirect, url_for, abort
import os
import watchlist
import stock_pred
import datetime as dt
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import OrderedDict

ROOTDIR = os.path.abspath(os.curdir)
plt.switch_backend('agg')

app = Flask(__name__, template_folder='templates')
companies = ['AAPL', 'SPY', 'MSFT', 'BTC-USD', 'ETH-USD', 'TSLA', 'NFLX', 'META', 'GOOG', 'AMZN']
charts = ['1W', '1M', '3M', '1Y']
predictions = ['Prediction']

@app.route('/')
def home():
    stock_responses = watchlist.get_stocks(companies)
    stock_prices = watchlist.get_current_prices(companies, stock_responses)
    watchlist.save_historical_data(companies[0])
    df = get_dataframe(companies[0])
    create_charts(companies[0])
    return render_template('index.html', companies=companies, charts=charts, prediction=predictions[0], result = OrderedDict(sorted(stock_prices.items())), tab=charts[1], tables=[df.to_html(index=False)], titles=[''])

def get_dataframe(company):
    file_to_open = os.path.join(ROOTDIR, 'market_data', company + '.csv')
    data = pd.read_csv(file_to_open, parse_dates=True, skipinitialspace=False)
    del data['Adj Close']
    df = data.round(2).sort_values('Date', ascending=False)
    return df

def create_charts(company):
    file_to_open = os.path.join(ROOTDIR, 'market_data', company + '.csv')
    df = pd.read_csv(file_to_open, parse_dates=True, skipinitialspace=False)
    df = df.sort_values('Date')
    df.index = pd.DatetimeIndex(df['Date'])

    current_date = dt.datetime.now()
    formatted_current_date = current_date.strftime('%Y-%m-%d')

    formatted_one_week_ago = (current_date - dt.timedelta(days=7)).strftime('%Y-%m-%d')
    formatted_one_month_ago = (current_date - dt.timedelta(days=30)).strftime('%Y-%m-%d')
    formatted_three_month_ago = (current_date - dt.timedelta(days=90)).strftime('%Y-%m-%d')
    formatted_one_year_ago = (current_date - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    try:
        # One Week Candlestick Chart
        tdf = df.loc[formatted_one_week_ago:formatted_current_date,:]
        mpf.plot(tdf, type='candlestick', style='yahoo', volume=True, tight_layout=True, figsize=(16,8), savefig=os.path.join(ROOTDIR, 'static', companies[0] + '_1w.png'))
        # One Month Candlestick Chart
        tdf = df.loc[formatted_one_month_ago:formatted_current_date,:]
        mpf.plot(tdf, type='candlestick', style='yahoo', volume=True, tight_layout=True, figsize=(16,8), savefig=os.path.join(ROOTDIR, 'static', companies[0] + '_1m.png'))
        # Three Month Candlestick Chart
        tdf = df.loc[formatted_three_month_ago:formatted_current_date,:]
        mpf.plot(tdf, type='candlestick', style='yahoo', volume=True, tight_layout=True, figsize=(16,8), savefig=os.path.join(ROOTDIR, 'static', companies[0] + '_3m.png'))
        # One Year Candlestick Chart
        tdf = df.loc[formatted_one_year_ago:formatted_current_date,:]
        mpf.plot(tdf, type='candlestick', style='yahoo', volume=True, tight_layout=True, figsize=(16,8), savefig=os.path.join(ROOTDIR, 'static', companies[0] + '_1y.png'))
    except Exception as e:
        print(e)
        pass

@app.route('/ticker/')
def ticker():
    if request.args.get('symbol'):
        symbols = request.args.get('symbol').strip().split(" ")
        for stock in reversed(symbols):
            stock = stock.strip().upper()
            if not stock:
                continue
            if stock in companies:
                companies.remove(stock)
            companies.insert(0, stock)
            if len(companies) > 10:
                companies.pop(10)
    return redirect("/")

@app.route('/predict/')
def predict():
    stock_pred.render_prediction(companies[0])
    stock_responses = watchlist.get_stocks(companies)
    stock_prices = watchlist.get_current_prices(companies, stock_responses)
    df = get_dataframe(companies[0])
    return render_template('index.html', companies=companies, charts=charts, prediction=predictions[0], result = OrderedDict(sorted(stock_prices.items())), tab=predictions[0], tables=[df.to_html(index=False)], titles=[''])

@app.route('/about')
def about():
    return redirect("/")
    # return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
