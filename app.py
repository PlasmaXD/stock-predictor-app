from flask import Flask, render_template, jsonify, request
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from api.api import fetch_data
from models.data_preprocessor import preprocess_data, create_sequences
import os
import numpy as np
import datetime

app = Flask(__name__)

# AVAILABLE_SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
# 予測可能な銘柄一覧を拡張
AVAILABLE_SYMBOLS = [
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'FB', 'BABA', 'TSM', 'V', 'JNJ',
    'WMT', 'PG', 'NVDA', 'DIS', 'MA', 'HD', 'NFLX', 'ADBE', 'PYPL', 'INTC',
    'CMCSA', 'VZ', 'KO', 'PEP', 'CSCO', 'PFE', 'MRK', 'ABT', 'XOM', 'CVX',
    'NKE', 'T', 'BA', 'HON', 'IBM', 'MMM', 'UNH', 'CRM', 'WBA', 'RTX'
]

def train_model(symbol):
    data = fetch_data(symbol)
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data.values.reshape(-1, 1))
    X, y = create_sequences(data_scaled)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)),
        LSTM(units=50),
        Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=50, batch_size=32)
    
    model.save(f'models/{symbol}_stock_prediction_model.h5')
    return model, scaler

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/symbols', methods=['GET'])
def get_symbols():
    return jsonify({'symbols': AVAILABLE_SYMBOLS})

@app.route('/predict', methods=['GET'])
def predict():
    symbol = request.args.get('symbol', default='AAPL', type=str)
    model_path = f'models/{symbol}_stock_prediction_model.h5'
    
    try:
        if os.path.exists(model_path):
            model = load_model(model_path)
            data = fetch_data(symbol)
            scaler = MinMaxScaler(feature_range=(0, 1))
            data_scaled = scaler.fit_transform(data.values.reshape(-1, 1))
        else:
            model, scaler = train_model(symbol)
            data = fetch_data(symbol)
            data_scaled = scaler.transform(data.values.reshape(-1, 1))
        
        X, _ = create_sequences(data_scaled)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        predictions_scaled = model.predict(X)
        predictions = scaler.inverse_transform(predictions_scaled)

        dates = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(len(predictions))]
        dates.reverse()
        
        return jsonify({'prices': predictions.tolist(), 'dates': [date.isoformat() for date in dates]})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
