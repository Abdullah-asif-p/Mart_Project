import uuid
from fastapi import HTTPException, status,Depends
from sqlmodel import Session, select
from .models import Product, ProductCreate, ProductUpdate
from .db import db_dependency
from app import producer, product_schema_pb2

KAFKA_BROKER = "broker:19092"
KAFKA_TOPIC = "todos"
KAFKA_CONSUMER_GROUP_ID = "kafkafast-container"


async def create_product(session: Session, product: ProductCreate , producer ):
    print("\n\n\nCreate_product....\n\n\n")
    try:
        id = str(uuid.uuid4())
        print("\n\n\n\Produced....\n\n\n")
        productproto = product_schema_pb2.Product(
            id=id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            stock=product.stock,
        )
        print(f"product : {productproto}")
        # productproto = product_schema_pb2.Product(add_product)
        serialized_product = productproto.SerializeToString()
        send_result = await producer.send_and_wait(KAFKA_TOPIC, value=serialized_product)
        print(f"Message sent: {send_result}")
        # session.add(add_product)
        # session.commit()
        # session.refresh(add_product)
        return productproto
    except Exception as e:
        # session.rollback()
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
