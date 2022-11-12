from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schema, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(tags=["Users"], prefix="/users")


@router.get("/", response_model=List[schema.User])
def get_users(
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.User).all()

    return posts


@router.get("/{id}", response_model=schema.User)
def get_user(
        id: int, db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} does not exist"
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_user(user_data: schema.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hash_password = utils.hash_password(user_data.password)
    user_data.password = hash_password
    new_user = models.User(**user_data.dict())
    db.add(new_user)
    db.commit()
    # retrive the new post stored into variable new post
    db.refresh(new_user)
    return new_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        id: int, db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    user_query = db.query(models.User).filter(models.User.id == id)

    if not user_query.first():
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} not found"
        )
    user_query.delete(synchronize_session=False)
    db.commit()
    return None
