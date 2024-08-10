import json
import uuid
from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from app.models.models import Product, ProductCreate, ProductRating, ProductUpdate
from app.models.inventory_model import InventoryItem
from app.core.db import db_dependency
from app.schema import product_schema_pb2


KAFKA_BROKER = "broker:19092"
KAFKA_TOPIC = "Product"
KAFKA_CONSUMER_GROUP_ID = "kafkafast-container"


async def create_product(session: Session, product: ProductCreate, producer):
    print("\nCreate_product....\n")
    try:
        id = str(uuid.uuid4())
        print("\nProduced....\n")
        # only one rating can be added

        productratingproto = product_schema_pb2.ProductRating(
            id=product.ratings.id, product_id=id, rating=product.ratings.rating, review=product.ratings.review)
        productproto = product_schema_pb2.Product(
            id=id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            stock=product.stock,
            ratings=productratingproto,
        )


        key = ("Created").encode("utf-8")
        product_dict = {
            field.name: getattr(productproto, field.name)
            for field in productproto.DESCRIPTOR.fields
        }
        serialized_product = productproto.SerializeToString()
        send_result = await producer.send_and_wait(
            KAFKA_TOPIC, value=serialized_product, key=key
        )
        # intailise inventory
        Inventorykey = ("Product Created").encode("utf-8")
        inventory_proto = product_schema_pb2.Intailise_Inventory(
            product_id=id, name=product.name, status="Not Available"
        )
        serialized_inventory = inventory_proto.SerializeToString()
        print(inventory_proto)
        print("43543",serialized_inventory)
        await producer.send_and_wait(
            "Initialise_Inventory", value=serialized_inventory, key=Inventorykey
        )

        print(f"Message sent: {send_result}")
        l = ProductRating.model_validate(product_dict["ratings"])
        print("\n\n\nl",l)
        product_response = Product.model_validate(product_dict)
        product_response.ratings = l
        print(product_response.ratings)
        return product_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"msg: {str(e)}"
        )


def get_product_by_id(session: db_dependency, product_id: str):
    return session.exec(select(Product).where(Product.id == product_id)).first()


def get_products(
    session: Session,
    category: str = None,
    price_min: float = None,
    price_max: float = None,
):
    query = select(Product)
    if category:
        query = query.where(Product.category == category)
    if price_min is not None:
        query = query.where(Product.price >= price_min)
    if price_max is not None:
        query = query.where(Product.price <= price_max)

    return session.exec(query).all()


async def update_product(
    session: db_dependency, product_id: str, product_data: ProductUpdate, producer
):
    get_product = session.exec(
        select(Product).where(Product.id == product_id)
    ).one_or_none()
    if get_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_data = product_data.model_dump(exclude_unset=True)
    product = get_product.sqlmodel_update(updated_data)
    p = product.model_dump()
    productproto = product_schema_pb2.Product(**p)
    key = ("Updated").encode("utf-8")
    print(f"product31 : {productproto}")
    serialized_product = productproto.SerializeToString()
    send_result = await producer.send_and_wait(
        KAFKA_TOPIC, value=serialized_product, key=key
    )
    print(f"Message sent: {send_result}")
    return updated_data


async def delete_product(session: db_dependency, product_id: str, producer):
    product = get_product_by_id(session, product_id)
    rating_statement = select(ProductRating).where(ProductRating.product_id == product_id)
    ratings = session.exec(rating_statement).all()
    for rating in ratings:
        session.delete(rating)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)  
    session.commit()
    p = product.model_dump()
    productproto = product_schema_pb2.Product(**p)
    Inventorykey = ("Product Deleted").encode("utf-8")
    print(f"product31 : {productproto}")
    Inventory = InventoryItem(
        id=None,name=product.name, product_id=product_id, quantity=0, status="Deleted"
    )
    i = product_schema_pb2.Intailise_Inventory(name=product.name, product_id=product_id,status="Deleted")
    serialized_inventory = i.SerializeToString()
    send_result1 = await producer.send_and_wait("Initialise_Inventory", value=serialized_inventory, key=Inventorykey)
    serialized_product = productproto.SerializeToString()
    send_result = await producer.send_and_wait(
        KAFKA_TOPIC, value=serialized_product, key=Inventorykey
    ) 
    print(f"Message sent: {send_result}")
    
    return True
