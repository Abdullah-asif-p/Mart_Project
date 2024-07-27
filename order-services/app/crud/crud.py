from datetime import datetime, timezone
import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.models import Order, OrderCreate, OrderUpdate
from app.core.db import db_dependency
from app.schema import  order_pb2
from app.core.producer import get_producer

KAFKA_BROKER = "broker:19092"
KAFKA_TOPIC = "orders"
KAFKA_CONSUMER_GROUP_ID = "kafkafast-container"

async def create_order(session: db_dependency, create_order: OrderCreate, user_id:str, producer):

    try:    
        # asignid = session.exec(select(Order).where(Order.id))
        id = str(uuid.uuid4())
        order = Order(
            id=id ,
            user_id= user_id,
            product_id= create_order.product_id,
            total_amount = create_order.total_amount,
            quantity = create_order.quantity,
            status = create_order.status,
        )
        date = str(order.created_at)
        print(str(order.created_at))
        prorder = order_pb2.Order(   
            id=id ,
            user_id= user_id,
            product_id= create_order.product_id,
            total_amount = int(create_order.total_amount),
            quantity = create_order.quantity,
            status = create_order.status,
            created_at=date)
        print(prorder)
        order_key = ("Order Created").encode()
        serialized_order = prorder.SerializeToString()
        send_result = await producer.send_and_wait(KAFKA_TOPIC, value=serialized_order , key=order_key)
        print(f"Message sent: {send_result}")
        return order
    except Exception as e:
        raise HTTPException(status_code=401,detail=f"Error:{str(e)}")
   

def get_order_by_id(session: db_dependency, order_id: int):
    return session.exec(select(Order).where(Order.id == order_id)).first()


async def update_order_status(session: db_dependency, order_id: str, orderup:OrderUpdate,producer):
    order = get_order_by_id(session, order_id)
    order_data = orderup.model_dump(exclude_unset=True)
    order.sqlmodel_update(order_data)
    p = order.model_dump()
    p['created_at'] = str(order.created_at)
    p['status'] = str(order.status.value)
    p['total_amount'] = int(order.total_amount)
    prorder = order_pb2.Order(**p)
    order_key = ("Order Updated").encode()
    serialized_order = prorder.SerializeToString()
    send_result = await producer.send_and_wait(KAFKA_TOPIC, value=serialized_order , key=order_key)
    print(f"Message sent: {send_result}")
    if not order:
        return None
    return order


def add_new_order(order_data: Order, session: Session):
    print("Adding Inventory Item to Database")
    session.add(order_data)
    session.commit()
    session.refresh(order_data)
    print(order_data)
    return order_data

def update_orders(data: Order, session: Session):
    print("Updated Inventory Item to Database")
    p = Order.model_validate(data)
    session.add(data)
    session.commit()
    session.refresh(data)
    print(p)
    return p

def get_orders_by_user_id(session: db_dependency, user_id: str):
    return session.exec(select(Order).where(Order.user_id == user_id)).all()
