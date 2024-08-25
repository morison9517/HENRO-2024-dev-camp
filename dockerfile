# ベースイメージとして公式のPythonイメージを使用
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なライブラリをインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . /app/

# ポートを開放
EXPOSE 8000

# コマンドを実行
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "HENRO.wsgi:application"]

RUN pip install --upgrade pip


