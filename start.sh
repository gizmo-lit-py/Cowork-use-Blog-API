#!/bin/bash
# コンテナ起動時にDBのテーブルを作成してからアプリを起動する
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
