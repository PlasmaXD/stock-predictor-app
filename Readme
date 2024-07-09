
### アプリケーションの機能

1. **株価の予測**:
   - ユーザーが指定した銘柄（例：AAPL、GOOGL、MSFTなど）の株価を予測します。
   - 過去の株価データを使用してLSTM（Long Short-Term Memory）モデルをトレーニングし、未来の株価を予測します。

2. **銘柄リストの表示**:
   - 利用可能な銘柄のリストを表示し、ユーザーがリストから銘柄を選択して予測を実行できます。

3. **任意の銘柄の予測**:
   - ユーザーが入力した任意の銘柄に対して予測を実行できます。

4. **予測結果のグラフ表示**:
   - 予測結果をグラフで表示し、視覚的に確認できます。

### 使用技術

- **フロントエンド**:
  - HTML, CSS, JavaScript
  - Chart.js：予測結果をグラフで表示するためのライブラリ

- **バックエンド**:
  - Flask：Pythonのウェブフレームワーク
  - TensorFlow：LSTMモデルを使用して株価を予測
  - Alpha Vantage API：株価データを取得
  - Python-dotenv：環境変数の管理

- **コンテナ化**:
  - Docker：アプリケーションをコンテナとしてパッケージ化
  - Docker Compose：複数のコンテナを簡単に管理

### プロジェクト構成

```
.
├── api
│   ├── __init__.py
│   └── api.py
├── app.py
├── config
│   ├── __init__.py
│   └── settings.py
├── Dockerfile
├── docker-compose.yml
├── models
│   ├── __init__.py
│   ├── data_preprocessor.py
│   ├── lstm_model.py
│   └── train_model.py
├── requirements.txt
├── static
│   ├── css
│   │   └── style.css
│   └── js
│       └── script.js
├── templates
│   └── index.html
├── tests
│   ├── __init__.py
│   ├── test_api.py
│   └── test_models.py
└── utils
    ├── __init__.py
    └── helper_functions.py
```

### 各ファイルの説明

- **api/api.py**: Alpha Vantage APIを使用して株価データを取得する機能を実装。
- **app.py**: Flaskアプリケーションのメインエントリーポイント。ルーティングや環境変数の読み込みを行う。
- **config/settings.py**: 環境変数からAPIキーを読み込む設定。
- **models/data_preprocessor.py**: データの前処理を行う関数を定義。
- **models/lstm_model.py**: LSTMモデルの定義。
- **models/train_model.py**: 指定された銘柄のモデルをトレーニングし、保存するスクリプト。
- **requirements.txt**: 必要なPythonパッケージのリスト。
- **static/css/style.css**: アプリケーションのスタイルシート。
- **static/js/script.js**: フロントエンドのJavaScript。銘柄リストの表示や予測結果のグラフ表示を担当。
- **templates/index.html**: アプリケーションのHTMLテンプレート。
- **tests/**: テストスクリプト。
- **utils/**: ヘルパー関数。

### コンテナ化

- **Dockerfile**: アプリケーションをコンテナ化するための設定ファイル。ベースイメージの指定、依存関係のインストール、アプリケーションの実行設定を記述。
- **docker-compose.yml**: 複数のコンテナを管理するための設定ファイル。Flaskアプリケーションのコンテナ設定を記述。

### 環境変数の管理

- **.env**: APIキーなどの秘密情報を管理。これを使用して環境変数を設定し、GitHubにアップロードしないように`.gitignore`に追加。

このアプリケーションは、株価予測を簡単に行うためのウェブベースのツールであり、コンテナ化することで一貫した環境で実行可能です。