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

        # logic for multiple ratings

        """productratings = []
        productratingsproto = []
        for rat in product.ratings:
            productrating = ProductRating(
                id= "1",
                product_id= id,
                rating=rat.rating,
                review=rat.review
            )
            productratingproto = product_schema_pb2.ProductRating(
                id="1", product_id=id, rating=rat.rating, review=rat.review
            )
            productratings.append(productrating)
            productratingsproto.append(productratingproto)"""

        productratingproto = product_schema_pb2.ProductRating(
            product_id=id, rating=product.ratings.rating, review=product.ratings.review)
        productproto = product_schema_pb2.Product(
            id=id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            stock=product.stock,
            ratings=productratingproto,
        )
        print("prot", productproto)
        # k = []
        # for r in productproto.rating:
        #     print(r)
        #     l = ProductRating.model_validate(r)
        #     k.append(l)
        #     print("vALI",l)
        # print("Ipc",k)

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
        Inventory = InventoryItem(product_id=id, quantity=0,name=productproto.name)
        item_dict = {field: getattr(Inventory, field) for field in Inventory.dict()}
        item_json = json.dumps(item_dict).encode("utf-8")
        send_result1 = await producer.send_and_wait(
            "Initialise_Inventory", value=item_json, key=Inventorykey
        )

        print(f"Message sent: {send_result}")
        l = ProductRating.model_validate(product_dict["ratings"])
        # product_dict["rating"] = l
        print("l",l)
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
    # print(query)
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
    if not product:
        return None
    p = product.model_dump()
    productproto = product_schema_pb2.Product(**p)
    key = ("Deleted").encode("utf-8")
    print(f"product31 : {productproto}")
    Inventory = InventoryItem(
        id=None, product_id=product_id, quantity=0, status="Deleted"
    )
    print(Inventory)
    item_dict = {field: getattr(Inventory, field) for field in Inventory.dict()}
    item_json = json.dumps(item_dict).encode("utf-8")
    send_result1 = await producer.send_and_wait("inventory", value=item_json, key=key)
    serialized_product = productproto.SerializeToString()
    send_result = await producer.send_and_wait(
        KAFKA_TOPIC, value=serialized_product, key=key
    )
    print(f"Message sent: {send_result}")
    print(productproto)
    return True
