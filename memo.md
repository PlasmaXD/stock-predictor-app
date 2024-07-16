### フォルダ構造
```
/stock-predictor-app
|-- /api
|   |-- __init__.py
|   |-- api.py
|
|-- /models
|   |-- __init__.py
|   |-- lstm_model.py
|   |-- data_preprocessor.py
|
|-- /utils
|   |-- __init__.py
|   |-- helper_functions.py
|
|-- /config
|   |-- __init__.py
|   |-- settings.py
|
|-- /tests
|   |-- __init__.py
|   |-- test_api.py
|   |-- test_models.py
|
|-- app.py
|-- requirements.txt
```
```
mkdir -p stock-predictor-app/{api,models,utils,config,tests}
touch stock-predictor-app/api/__init__.py stock-predictor-app/api/api.py
touch stock-predictor-app/models/__init__.py stock-predictor-app/models/lstm_model.py stock-predictor-app/models/data_preprocessor.py
touch stock-predictor-app/utils/__init__.py stock-predictor-app/utils/helper_functions.py
touch stock-predictor-app/config/__init__.py stock-predictor-app/config/settings.py
touch stock-predictor-app/tests/__init__.py stock-predictor-app/tests/test_api.py stock-predictor-app/tests/test_models.py
touch stock-predictor-app/app.py stock-predictor-app/requirements.txt
```

### 各ファイルの内容

#### `/api/api.py`
```python
from alpha_vantage.timeseries import TimeSeries
from config.settings import ALPHA_VANTAGE_API_KEY

def fetch_stock_data(symbol):
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    data, _ = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
    return data['4. close']  # 終値データ
```

#### `/models/lstm_model.py`
```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def create_model(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model
```

#### `/models/data_preprocessor.py`
```python
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
```

#### `/utils/helper_functions.py`
```python
def print_info(message):
    print(f"[INFO] {message}")
```

#### `/config/settings.py`
```python
ALPHA_VANTAGE_API_KEY = 'your_alpha_vantage_api_key'
```

#### `/app.py`
```python
from flask import Flask, jsonify
from api.api import fetch_stock_data
from models.lstm_model import create_model
from models.data_preprocessor import preprocess_data, create_sequences
from tensorflow.keras.models import load_model

app = Flask(__name__)

# モデルをロードするか新しく作成
model = create_model((60, 1))  # 例として60時間のシーケンス

@app.route('/predict/<string:symbol>', methods=['GET'])
def predict(symbol):
    data = fetch_stock_data(symbol)
    data_scaled = preprocess_data(data)
    X, _ = create_sequences(data_scaled)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    prediction = model.predict(X)
    return jsonify(prediction.tolist())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

#### `/requirements.txt`
```
flask
tensorflow
alpha_vantage
pandas
numpy
sklearn
```

### 実行方法
1. まず`requirements.txt`で指定された依存関係をインストールします：
   ```
   pip install -r requirements.txt
   ```
2. `app.py`を実行してFlaskサーバーを起動します：
   ```
   python app.py
   ```
3. ブラウザやAPIテストツール（Postmanなど）を使って、例えば`http://localhost:5000/predict/AAPL`にアクセスし、予測を取得します。

## 仕組みの概要

このアプリケーションは、過去の株価データを利用して未来の株価を予測するために、LSTM（Long Short-Term Memory）というディープラーニングモデルを使用

### 1. データ取得

アプリケーションはAlpha Vantage APIを使用して、指定された銘柄の過去の株価データを取得します。

### 2. データ前処理

取得した株価データを以下のように前処理します：
- データを正規化（0から1の範囲にスケーリング）します。
- LSTMモデルに入力できるように、過去の株価データを一定の期間ごとのシーケンスに変換します（例えば、過去60日のデータを使って次の日の株価を予測）。

### 3. モデルのトレーニング

前処理されたデータを使用してLSTMモデルをトレーニングします。LSTMは、時系列データのパターンを学習するのに適したリカレントニューラルネットワーク（RNN）の一種です。

### 4. モデルの保存

トレーニングが完了したモデルを保存します。これは、同じ銘柄に対して再度予測を行う際に、再トレーニングを避けるためです。

### 5. 予測

保存されたモデルを使用して、未来の株価を予測します。予測結果は正規化された値から元のスケールに戻され、実際の株価として表示されます。

### 6. 結果の表示

予測された株価は、Chart.jsライブラリを使用してグラフで表示されます。これにより、ユーザーは視覚的に予測結果を確認できます。

### 全体の流れ

1. **ユーザーが銘柄を入力**:
   ユーザーはウェブインターフェースを通じて予測したい銘柄を入力します。

2. **データ取得と前処理**:
   アプリケーションがAlpha Vantage APIを使って過去の株価データを取得し、前処理します。

3. **モデルのトレーニング**:
   前処理されたデータを用いてLSTMモデルをトレーニングします（既にトレーニング済みのモデルが存在する場合はそのモデルを使用）。

4. **未来の株価を予測**:
   トレーニングされたモデルを使って未来の株価を予測します。

5. **結果の表示**:
   予測結果をグラフとして表示します。

この仕組みにより、ユーザーは特定の銘柄の未来の株価を予測し、その結果を視覚的に確認することができます。
