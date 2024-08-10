from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.auth import login_for_access_token,UserDep
import stripe
from app.crud import curd

router = APIRouter()


@router.get("/")
def root():
    return{"hello","world"}

@router.post("/login")
def get_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        return login_for_access_token(form_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-payment-intent/")
async def create_payment(amount: int,user:UserDep):
    curd.create_payment_intent(amount=amount,user=user["user_id"])
