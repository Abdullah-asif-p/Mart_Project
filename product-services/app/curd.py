import uuid
from fastapi import HTTPException, status
from sqlmodel import Session, select
from .models import Product, ProductCreate, ProductUpdate
from .db import db_dependency


def create_product(session: Session, product: ProductCreate ):
    try:
        id = str(uuid.uuid4())
        existing_id = session.exec(select(Product).where(Product.id == id)).first()
        if existing_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is already registered you may need to update or delete the existing product",
            )
      
        add_product = Product(
            id=id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            stock=product.stock,
        )
        session.add(add_product)
        session.commit()
        session.refresh(add_product)
        return add_product
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def get_product_by_id(session: db_dependency, product_id: str):
    return session.exec(select(Product).where(Product.id == product_id)).first()




def get_products(
    session:Session,
    category: str = None,
    price_min: float = None,
    price_max: float = None,
):

 
    # query = select(Product)
    if category:
        query = select(Product).where(Product.category == category)
    if price_min is not None:
        query = select(Product).where(Product.price >= price_min)
    if price_max is not None:
        query = select(Product).where(Product.price <= price_max)
    # print(query)
    return session.exec(select(Product).where(Product.category == category)).all()


def update_product(session: db_dependency, product_id: str, product_data: ProductUpdate):
    product = get_product_by_id(session, product_id)
    if not product:
        return None
    for key, value in product_data.items():
        setattr(product, key, value)
    session.commit()
    session.refresh(product)
    return product


def delete_product(session: db_dependency, product_id: str):
    product = get_product_by_id(session, product_id)
    if not product:
        return None
    session.delete(product)
    session.commit()
    session.refresh(product)
    return {"message":"Product deleted successfully"}
