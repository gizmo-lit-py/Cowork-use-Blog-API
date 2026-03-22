from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# ===== ユーザー関連 =====

class UserCreate(BaseModel):
    """ユーザー登録のリクエスト形式"""
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    """ユーザー情報のレスポンス形式（パスワードは返さない！）"""
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemyのモデルをそのまま変換できるようにする


# ===== 認証関連 =====

class Token(BaseModel):
    """ログイン成功時に返すトークン"""
    access_token: str
    token_type: str  # 常に "bearer"


# ===== タグ関連 =====

class TagCreate(BaseModel):
    """タグ作成のリクエスト形式"""
    name: str


class TagResponse(BaseModel):
    """タグのレスポンス形式"""
    id: int
    name: str

    class Config:
        from_attributes = True


# ===== 記事関連 =====

class PostCreate(BaseModel):
    """記事作成のリクエスト形式"""
    title: str
    content: str
    tag_ids: Optional[List[int]] = []  # タグのIDリスト（任意）


class PostUpdate(BaseModel):
    """記事更新のリクエスト形式（全部任意項目）"""
    title: Optional[str] = None
    content: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class PostResponse(BaseModel):
    """記事のレスポンス形式"""
    id: int
    title: str
    content: str
    author: UserResponse
    tags: List[TagResponse]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
