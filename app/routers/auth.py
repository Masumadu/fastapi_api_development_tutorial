from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema, models, database, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
    tags=["Authentication"],
    prefix="/users"
)


@router.post("/login", response_model=schema.Token)
def user_login(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"invalid credentials"
        )
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}



