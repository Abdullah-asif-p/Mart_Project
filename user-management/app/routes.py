from datetime import timedelta
from typing import Annotated, List
import uuid
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlmodel import select
from .helperfunc import authenticate_superadmin, authenticate_user, create_access_token
from .models import (
    ChangeEmail,
    SuperAdmin,
    Token,
    Users,
    UserCreate,
    ChangePassword,
    ChangeUsername,
)
from .db import db_dependency
from .helperfunc import user_dependency

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication Failed")
        if user["role"] == "User":
            return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/admin", status_code=status.HTTP_200_OK)
async def user(user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication Failed")
        if user["role"] == "Admin":
            return user
        else:
            raise HTTPException(status_code=401, detail="Authentication Failed")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/token/", response_model=Token)
async def login_for_access(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate the user",
            )

        token = create_access_token(
            username=user["username"],
            user_id=user["user_id"],
            email=user["email"],
            role=user["role"],
            expires_delta=timedelta(hours=24),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"good {str(e)}"
        )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/admintoken/", response_model=Token)
async def login_for_access(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate the admin",
            )
        if user["role"] == "Admin":
            token = create_access_token(
                username=user["username"],
                user_id=user["user_id"],
                email=user["email"],
                role=user["role"],
                expires_delta=timedelta(hours=24),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate the admin",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"good {str(e)}"
        )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/add_admin", status_code=status.HTTP_201_CREATED)
async def signup(
    superadminusername: Annotated[str, Form()],
    superadminpassword: Annotated[str, Form()],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: db_dependency,
):
    authenticated = authenticate_superadmin(superadminusername, superadminpassword)
    if not authenticated:
        raise HTTPException(status_code=402, detail="Unauthorized")
    hashed_password = pwd_context.hash(password)
    user_id = str(uuid.uuid4())
    existing_user = session.exec(
        select(Users).where(Users.username == username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    create_user_model = Users(
        user_id=user_id,
        role="Admin",
        email="admin@admin.com",
        username=username,
        hashed_password=hashed_password,
    )

    try:
        session.add(create_user_model)
        session.commit()
        session.refresh(create_user_model)
    except Exception as e:

        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/singup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, session: db_dependency):
    hashed_password = pwd_context.hash(user_data.password)
    user_id = str(uuid.uuid4())
    existing_user = session.exec(
        select(Users).where(Users.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    create_user_model = Users(
        user_id=user_id,
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
    )

    try:
        session.add(create_user_model)
        session.commit()
        session.refresh(create_user_model)
    except Exception as e:

        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/update_username")
async def update_username(
    new_username: ChangeUsername, session: db_dependency, current_user: user_dependency
):
    """
    Update own username.
    """
    # user_data = new_username
    user = session.get(Users, current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user = session.exec(
        select(Users).where(Users.username == new_username.new_username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already taken")

    user.username = new_username.new_username
    current_user["username"] = user.username
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"message": "Username updated successfully"}


@router.put("/update_password")
async def update_pass(
    user_data: ChangePassword, session: db_dependency, current_user: user_dependency
):

    user = session.get(Users, current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = pwd_context.hash(user_data.new_password)
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"message": "Password updated successfully"}


@router.put("/update_email")
async def update_username(
    new_email: ChangeEmail, session: db_dependency, current_user: user_dependency
):
    user = session.get(Users, current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = new_email.email
    current_user["email"] = user.email
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"message": "Email updated successfully"}


@router.post(
    "/delete_user",
)
async def delete_current_user(
    password: ChangePassword, session: db_dependency, current_user: user_dependency
):

    user = authenticate_user(current_user["username"], password.new_password, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        userobj = session.get(Users, current_user["user_id"])
        session.delete(userobj)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"message": "User deleted successfully"}
