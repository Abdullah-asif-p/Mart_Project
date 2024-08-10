from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.db import db_dependency
from app.kafka.producer import get_producer
from app.core.auth import login_for_access_token,UserDep
from app.models.notification import Notifications
from app.crud import curd
router = APIRouter()


@router.get("/")
def root():
    return {"hello": "world"}


@router.post("/login")
def get_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        return login_for_access_token(form_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/read")
def read_notifications( session: db_dependency, user: UserDep):
    userid = user["user_id"]
    print(userid)
    Notification = curd.get_notifications(session, userid)
    if not Notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return Notification
