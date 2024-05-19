from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.io as pio
from model import create_features, train_model
from data_ingestion import preprocess_data, fetch_stock_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    ticker = request.form['ticker']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    raw_data = fetch_stock_data(ticker, start_date, end_date)
    processed_data = preprocess_data(raw_data)
    feature_data = create_features(processed_data)
    model = train_model(feature_data)

    last_return = feature_data['Return'].iloc[-1]
    prediction = model.predict(np.array([[last_return]]))[0]

    fig = px.line(processed_data, x=processed_data.index, y='Close', title=f'{ticker} Stock Price')
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('predict.html', prediction=prediction, graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)
