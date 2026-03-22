from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.routers.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["記事"])


@router.post("/", response_model=schemas.PostResponse, status_code=201)
def create_post(
    post_data: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # ログイン必須
):
    """記事を作成する"""
    new_post = models.Post(
        title=post_data.title,
        content=post_data.content,
        author_id=current_user.id,
    )

    # タグを設定する
    if post_data.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(post_data.tag_ids)).all()
        new_post.tags = tags

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """記事一覧を取得する（ページネーション付き）"""
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """特定の記事を1件取得する"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="記事が見つかりません")
    return post


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post_data: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # ログイン必須
):
    """記事を更新する（自分の記事のみ）"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="記事が見つかりません")

    # 自分の記事じゃなかったら弾く
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="他のユーザーの記事は編集できません")

    # 送られてきた項目だけ更新する
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    if post_data.tag_ids is not None:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(post_data.tag_ids)).all()
        post.tags = tags

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # ログイン必須
):
    """記事を削除する（自分の記事のみ）"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="記事が見つかりません")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="他のユーザーの記事は削除できません")

    db.delete(post)
    db.commit()
