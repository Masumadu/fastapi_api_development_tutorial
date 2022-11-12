from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = settings.secret_key
ALGORITHMS = settings.algorithm
TOKEN_EXPIRATION_TIME = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHMS)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHMS)
        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token=token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
