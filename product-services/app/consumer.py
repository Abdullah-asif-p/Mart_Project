from aiokafka import AIOKafkaConsumer
from fastapi import HTTPException
# from sqlmodel import  Session
from app.models import Product
from app import product_schema_pb2
from .db import get_db

KAFKA_BROKER = "broker:19092"
KAFKA_TOPIC = "todos"
# KAFKA_CONSUMER_GROUP_ID = "kafkafast-container"

async def consume_messages(topic:str=KAFKA_TOPIC):
    # Create a consumer instance.
    consumer1 = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id="my-group",
        auto_offset_reset="earliest",
    )
   

    # Start the consumer.
    await consumer1.start()
    print("\n\n\nStart\n\n\n")
    try:
        # Continuously listen for messages.
        async for message in consumer1:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")
            new_product = product_schema_pb2.Product()
            new_product.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_product}")
            with next(get_db()) as session:
                product = Product(id=new_product.id,name=new_product.name , description=new_product.description,price=new_product.price, category=new_product.category ,stock=new_product.stock)
                session.add(product)
                session.commit()
                session.refresh(product)
                # session.add(new_product)
                # session.commit()
                # session.refresh(new_product)
            print("Done")

    except Exception as e:
        raise HTTPException(status_code=500, detail=(str(e)))
    finally:
        await consumer1.stop()