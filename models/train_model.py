import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from alpha_vantage.timeseries import TimeSeries
from config.settings import ALPHA_VANTAGE_API_KEY

def fetch_data(symbol):
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
    return data['4. close']  # 終値を取得

def preprocess_data(data, sequence_length=60):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data.values.reshape(-1, 1))

    X, y = [], []
    for i in range(sequence_length, len(data_scaled)):
        X.append(data_scaled[i-sequence_length:i, 0])
        y.append(data_scaled[i, 0])
    return np.array(X), np.array(y)

def build_model(input_shape):
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=input_shape),
        LSTM(units=50),
        Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def main(symbol):
    # データの取得
    data = fetch_data(symbol)
    
    # データの前処理
    X, y = preprocess_data(data)
    
    # モデルの構築
    model = build_model((X.shape[1], 1))
    
    # モデルのトレーニング
    model.fit(X, y, epochs=50, batch_size=32)
    
    # モデルの保存
    model.save(f'models/{symbol}_stock_prediction_model.h5')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python train_model.py <stock_symbol>")
    else:
        main(sys.argv[1])
