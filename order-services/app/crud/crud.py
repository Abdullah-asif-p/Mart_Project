from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import select
from app.models.models import Order, OrderCreate
from app.core.db import db_dependency
from app.schema import  order_pb2
from app.core import producer

KAFKA_BROKER = "broker:19092"
KAFKA_TOPIC = "todos"
KAFKA_CONSUMER_GROUP_ID = "kafkafast-container"

async def create_order(session: db_dependency, create_order: OrderCreate, user_id:str):

    try:    
        # asignid = session.exec(select(Order).where(Order.id))
        order = Order(
            user_id= user_id,
            product_id= create_order.product_id,
            total_amount = create_order.total_amount,
            quantity = create_order.quantity,
            status = create_order.status,
        )
        prorder = order_pb2.Order(**order)
        serialized_todo = prorder.SerializeToString()
        send_result = await producer.send_and_wait(KAFKA_TOPIC, value=serialized_todo)
        print(f"Message sent: {send_result}")
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
    except Exception as e:
        raise HTTPException(status_code=401,detail=f"Error:{str(e)}")
   

def get_order_by_id(session: db_dependency, order_id: int):
    return session.exec(select(Order).where(Order.id == order_id)).first()


def update_order_status(session: db_dependency, order_id: str, status: str):
    order = get_order_by_id(session, order_id)
    if not order:
        return None
    order.status = status
    session.commit()
    session.refresh(order)
    return order


def get_orders_by_user_id(session: db_dependency, user_id: str):
    return session.exec(select(Order).where(Order.user_id == user_id)).all()
