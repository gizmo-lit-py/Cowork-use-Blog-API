# ベースイメージ（Python 3.13を使う）
FROM python:3.13-slim

# コンテナ内の作業ディレクトリを設定
WORKDIR /app

# まずrequirements.txtだけコピーしてインストール（キャッシュを活かすため）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードを全部コピー
COPY . .

# FastAPIを起動（0.0.0.0はコンテナ外からアクセスできるようにするため）
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]
