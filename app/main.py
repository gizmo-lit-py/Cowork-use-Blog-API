from fastapi import FastAPI
from app.routers import auth, posts, tags

# FastAPIアプリの本体
app = FastAPI(
    title="ブログAPI",
    description="FastAPI + PostgreSQLで作ったブログAPI",
    version="1.0.0",
)

# 各ルーターを登録する
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(tags.router)


@app.get("/")
def root():
    """ヘルスチェック用のエンドポイント"""
    return {"message": "ブログAPIが動いています！"}
