from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models.models import Product, ProductCreate, ProductRating, ProductUpdate
from app.core.auth import  login_for_access_token
from app.curd import curd
from app.api.deps import get_producer, db_dependency, AdminDep


router = APIRouter()


@router.post("/login")
def get_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        return login_for_access_token(form_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create_products/")
async def add_product(
    product: ProductCreate,
    session: db_dependency,
    getproducer: get_producer,
):
    print(product)
    return await curd.create_product(session=session, product=product,producer=getproducer)


@router.get("/get_all_products/", response_model=list[Product])
def list_products(
    # admin: AdminDep,
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
async def modify_product(
    product_id: str,
    product_data: ProductUpdate,
    session: db_dependency,
    getproducer: get_producer,
):
    product = await curd.update_product(session, product_id, product_data, getproducer)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/delete_products/{product_id}")
async def remove_product(
    product_id: str,
    session: db_dependency,
    admin: AdminDep,
    getproducer: get_producer
):
    product = await curd.delete_product(session, product_id, getproducer)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted Successfully"}
