from datetime import timedelta
from typing import Annotated, List
import uuid
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import requests
from sqlmodel import Field, SQLModel, Session, select
from .db import db_dependency
from .models import Order, OrderCreate
from app import curd
from .auth import UserDep, login_for_access_token


router = APIRouter()
@router.post("/login")
def get_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        return login_for_access_token(form_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/orders/", response_model=Order)
def add_order(order: OrderCreate, session: db_dependency,user:UserDep):
    print(user)
    try:
        return curd.create_order(session, order,user)
    except Exception as e:
        raise HTTPException(status_code=401,detail=f"Error:{str(e)}")


@router.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int, session: db_dependency, user: UserDep):
    order = curd.get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=Order)
def modify_order(order_id: str, status: str, session: db_dependency, user: UserDep):
    order = curd.update_order_status(session, order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/orders", response_model=list[Order])
def list_orders(session: db_dependency,user:UserDep):
    return curd.get_orders_by_user_id(session, user)
