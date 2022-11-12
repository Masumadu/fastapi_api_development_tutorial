from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schema, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(tags=["Posts"], prefix="/posts")


@router.get("/", response_model=List[schema.PostVote])
def get_posts(
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user),
        limit: int = 10, skip: int = 0, search: Optional[str] = ""
):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()
    # print(results)
    return posts
    # return posts


@router.get("/{id}", response_model=schema.PostVote)
def get_post(
        id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(
        post_data: schema.PostCreate,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    new_post = models.Post(owner_id=current_user.id, **post_data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.patch("/{id}", response_model=schema.Post)
def update_post(
        post_data: schema.PostCreate, id: int,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"not authorized to perform requested action"
        )
    post_query.update(post_data.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        id: int,
        db: Session = Depends(get_db),
        current_user = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"not authorized to perform requested action"
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return None
