import yfinance as yf
import pandas as pd
import numpy as np

def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def preprocess_data(data):
    data['Return'] = data['Close'].pct_change()
    data.dropna(inplace=True)
    return data

if __name__ == "__main__":
    ticker = 'AAPL'
    start_date = '2022-01-01'
    end_date = '2023-01-01'
    raw_data = fetch_stock_data(ticker, start_date, end_date)
    processed_data = preprocess_data(raw_data)
    print(processed_data.head())
