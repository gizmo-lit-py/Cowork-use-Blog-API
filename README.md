# ブログAPI

FastAPI + PostgreSQL + Docker で構築したブログAPIです。

## 使用技術

- **FastAPI** - Pythonのモダンなウェブフレームワーク
- **PostgreSQL** - データベース
- **SQLAlchemy** - ORM（PythonでDBを操作するためのライブラリ）
- **Alembic** - DBマイグレーション管理
- **JWT** - 認証トークン
- **Docker / Docker Compose** - 環境構築

## 設計の判断メモ

- **DBにPostgreSQLを採用した理由**: 実務での利用率が高く、SQLiteと違い本番環境でも使えるスケーラブルなRDBMSのため
- **認証にJWTを採用した理由**: ステートレスな認証を実現でき、スケールしやすいため。セッション管理をサーバー側に持たなくてよい
- **タグを多対多で設計した理由**: 1つの記事に複数タグ・1つのタグが複数記事に使われる関係を正規化して表現するため
- **ルーターをファイル分割した理由**: 機能ごとに責務を分離し、コードの見通しをよくするため

## 起動方法

```bash
docker compose up --build
```

## APIエンドポイント

| メソッド | パス | 説明 | 認証 |
|--------|------|------|------|
| POST | /auth/register | ユーザー登録 | 不要 |
| POST | /auth/login | ログイン | 不要 |
| GET | /posts | 記事一覧 | 不要 |
| GET | /posts/{id} | 記事詳細 | 不要 |
| POST | /posts | 記事作成 | 必要 |
| PUT | /posts/{id} | 記事更新 | 必要 |
| DELETE | /posts/{id} | 記事削除 | 必要 |
| GET | /tags | タグ一覧 | 不要 |
| POST | /tags | タグ作成 | 必要 |

## APIドキュメント

起動後に http://localhost:8000/docs にアクセスすると、Swagger UIでAPIを確認・テストできます。

## 開発について

本プロジェクトはClaude（AI）を活用して開発しました。
設計判断（DB設計・認証方式・ルーター構成）は自分で考え、
コードの実装をAIと一緒に進めるスタイルで開発しています。
