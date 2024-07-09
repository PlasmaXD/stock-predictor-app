import numpy as np
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))

def preprocess_data(data):
    data_scaled = scaler.fit_transform(data.values.reshape(-1, 1))
    return data_scaled

def create_sequences(data_scaled, sequence_length=60):
    x, y = [], []
    for i in range(len(data_scaled) - sequence_length - 1):
        x.append(data_scaled[i:(i + sequence_length), 0])
        y.append(data_scaled[i + sequence_length, 0])
    return np.array(x), np.array(y)
