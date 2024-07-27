from datetime import timedelta
from typing import Annotated, List
import uuid
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import requests
from sqlmodel import Field, SQLModel, Session, select
from app.core.db import db_dependency
from app.models.models import Order, OrderCreate, OrderUpdate
from app.crud import crud
from app.api.auth import UserDep, login_for_access_token
from app.core.producer import get_producer

router = APIRouter()
@router.post("/login")
def get_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        return login_for_access_token(form_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/orders/")
async def add_order(order: OrderCreate, session: db_dependency,user:UserDep, getproducer:get_producer ):
   
    try:
        return await crud.create_order(session, order,user['user_id'],producer=getproducer)
    except Exception as e:
        raise HTTPException(status_code=401,detail=f"Error:{str(e)}")




@router.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: str, session: db_dependency, user: UserDep):
    order = crud.get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=Order)
async def modify_order(order_id: str, order: OrderUpdate, session: db_dependency, user: UserDep, getproducer:get_producer):
    order = await crud.update_order_status(session, order_id, order,producer=getproducer)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order


@router.post("/list", response_model=list[Order])
def list_orders(session: db_dependency,user:UserDep):
    return crud.get_orders_by_user_id(session, user['user_id'])
