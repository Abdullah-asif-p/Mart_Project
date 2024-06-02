from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .models import Product, ProductCreate, ProductUpdate
from .db import db_dependency
from .auth import AdminDep, login_for_access_token
from app import curd


router = APIRouter()


@router.post("/login")
def get_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        return login_for_access_token(form_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create_products/", response_model=Product)
def add_product(product: ProductCreate, session: db_dependency, admin: AdminDep):
    print(admin,"admin")
    return curd.create_product(session, product)


@router.get("/get_all_products/", response_model=list[Product])
def list_products(
    admin: AdminDep,
    session: db_dependency,
    category: str = None,
    price_min: float = None,
    price_max: float = None,
):

    return curd.get_products(
        session=session, category=category, price_min=price_min, price_max=price_max
    )


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: str, session: db_dependency, admin: AdminDep):
    product = curd.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/update_products/{product_id}", response_model=Product)
def modify_product(
    product_id: str, product_data: ProductUpdate, session: db_dependency
):
    product = curd.update_product(session, product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/delete_products/{product_id}")
def remove_product(product_id: str, session: db_dependency, admin: AdminDep):
    product = curd.delete_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted Successfully"}
