from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# 記事とタグの中間テーブル（多対多の関係を実現するため）
# 例：記事Aに「Python」「初心者」のタグが付く
#     「Python」タグは記事A・記事Bに使われる
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class User(Base):
    """ユーザーテーブル"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # パスワードは必ずハッシュ化して保存
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # このユーザーが書いた記事一覧（postsテーブルと繋がる）
    posts = relationship("Post", back_populates="author")


class Post(Base):
    """記事テーブル"""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))  # どのユーザーが書いたか
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 作者情報（usersテーブルと繋がる）
    author = relationship("User", back_populates="posts")
    # タグ一覧（中間テーブル経由でtagsテーブルと繋がる）
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")


class Tag(Base):
    """タグテーブル"""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # このタグが付いた記事一覧（中間テーブル経由）
    posts = relationship("Post", secondary=post_tags, back_populates="tags")
