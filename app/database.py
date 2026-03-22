import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 環境変数からDBのURLを取得（docker-compose.ymlで設定したやつ）
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/blogdb")

# DBエンジンを作成（実際のDB接続の本体）
engine = create_engine(DATABASE_URL)

# セッション（DB操作のひとまとまり）を作るファクトリ
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルの基底クラス（models.pyでこれを継承してテーブルを定義する）
Base = declarative_base()


# APIの各エンドポイントでDB接続を使えるようにする関数
# FastAPIの「依存性注入」という仕組みで使う
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # 処理が終わったら必ず接続を閉じる
