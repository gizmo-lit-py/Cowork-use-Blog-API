from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.routers.auth import get_current_user

router = APIRouter(prefix="/tags", tags=["タグ"])


@router.post("/", response_model=schemas.TagResponse, status_code=201)
def create_tag(
    tag_data: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # ログイン必須
):
    """タグを作成する"""
    # 同じ名前のタグが既にあったら弾く
    if db.query(models.Tag).filter(models.Tag.name == tag_data.name).first():
        raise HTTPException(status_code=400, detail="そのタグはすでに存在します")

    new_tag = models.Tag(name=tag_data.name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@router.get("/", response_model=List[schemas.TagResponse])
def get_tags(db: Session = Depends(get_db)):
    """タグ一覧を取得する"""
    return db.query(models.Tag).all()
