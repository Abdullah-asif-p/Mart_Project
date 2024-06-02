from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from .models import CurrentUser, Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app import settings
from .db import db_dependency


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


def authenticate_user(username: str, password: str, db: Session):
    try:
        user: Users = db.exec(select(Users).where(Users.username == username)).first()
        if not user:
            return False
        if not pwd_context.verify(password, user.hashed_password):
            return False
        return {"user_id": user.user_id, "username": user.username, "email": user.email,"role":user.role}
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"auth user:{str(e)}")


def authenticate_superadmin(username: str, password: str):
    try:
        if (username == settings.USERNAME) and (password, settings.PASSWORD):
            return True
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"auth user:{str(e)}")


def create_access_token(
    username: str, user_id: str, email: str,role:str, expires_delta: timedelta | None = None
):
    data = {"sub": username, "id": user_id, "email": email, "role":role}
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=120)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)])-> CurrentUser:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = str(payload.get("sub"))
        user_id: str = str(payload.get("id"))
        email: str = str(payload.get("email"))
        role: str = str(payload.get("role"))
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate the user",
            )
        user: CurrentUser = {
            "username": username,
            "user_id": user_id,
            "email": email,
            "role": role,
        }
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


user_dependency = Annotated[dict, Depends(get_current_user)]
