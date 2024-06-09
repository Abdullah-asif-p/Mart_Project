import uuid
from fastapi import HTTPException, status,Depends
from sqlmodel import Session, select
from app.models.models import Product, ProductCreate, ProductUpdate
from app.core.db import db_dependency
from app.schema import  product_schema_pb2


KAFKA_BROKER = "broker:19092"
KAFKA_TOPIC = "todos"
KAFKA_CONSUMER_GROUP_ID = "kafkafast-container"


async def create_product(session: Session, product: Product , producer ):
    print("\n\n\nCreate_product....\n\n\n")
    try:
        id = str(uuid.uuid4())
        print("\n\n\nProduced....\n\n\n")
        # ratings =[] 
        # for rating in product.ratings:
        #     r = rating.model_dump()
        #     print(r)
        #     r["id"] = id
        #     # print(rating.model_dump())
        #     changes = product_schema_pb2.ProductRating(**r
        #         # id=rating["id"],
        #         # product_id=rating["product_id"],
        #         # rating=rating["rating"],
        #         # review=rating["review"],
        #     )
        #     ratings.append(changes)
        #     print(rating)
        # if ratings:
        #     print(rating)
        productproto = product_schema_pb2.Product(
            id=id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            stock=product.stock,
            ratings = product.ratings
        )
        key = ("Created").encode('utf-8')
        print(f"product : {productproto}")
        product_dict = {field.name: getattr(productproto, field.name) for field in productproto.DESCRIPTOR.fields}
        serialized_product = productproto.SerializeToString()
        send_result = await producer.send_and_wait(KAFKA_TOPIC, value=serialized_product,key=key)
        print(f"Message sent: {send_result}")
        return Product(**product_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"msg: {str(e)}"
        )


def get_product_by_id(session: db_dependency, product_id: str):
    return session.exec(select(Product).where(Product.id == product_id)).first()


def get_products(
    session:Session,
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
    send_result = await producer.send_and_wait(KAFKA_TOPIC, value=serialized_product,key=key)
    print(f"Message sent: {send_result}")
    return updated_data


async def delete_product(session: db_dependency, product_id: str,producer):
    product = get_product_by_id(session, product_id)
    if not product:
        return None
    p = product.model_dump()
    productproto = product_schema_pb2.Product(**p)
    key = ("Deleted").encode("utf-8")
    print(f"product31 : {productproto}")
    serialized_product = productproto.SerializeToString()
    send_result = await producer.send_and_wait(KAFKA_TOPIC, value=serialized_product,key=key)
    print(f"Message sent: {send_result}")
    print(productproto)
    return True
