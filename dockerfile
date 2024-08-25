# Python の公式イメージをベースにする
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要なライブラリをインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトのコードをコンテナにコピー
COPY . .

# 環境変数の設定
ENV PYTHONUNBUFFERED=1

# Django のマイグレーションを適用し、アプリケーションを起動するコマンドを設定
CMD ["sh", "-c", "python manage.py migrate && gunicorn HENRO.wsgi:application --bind 0.0.0.0:8000"]

