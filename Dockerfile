# ベースイメージとしてPython 3.11を使う
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# デモスクリプトをコピー
COPY crack_demo.py .

# コンテナ起動時にスクリプトを実行
CMD ["python", "crack_demo.py"]
