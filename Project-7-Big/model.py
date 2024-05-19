from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

def create_features(data):
    data['Lag_1'] = data['Return'].shift(1)
    data.dropna(inplace=True)
    return data

def train_model(data):
    X = data[['Lag_1']]
    y = data['Return']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')

    return model

if __name__ == "__main__":
    from data_ingestion import preprocess_data, fetch_stock_data

    ticker = 'AAPL'
    start_date = '2022-01-01'
    end_date = '2023-01-01'
    raw_data = fetch_stock_data(ticker, start_date, end_date)
    processed_data = preprocess_data(raw_data)
    feature_data = create_features(processed_data)
    model = train_model(feature_data)
