import json
from aiokafka import AIOKafkaConsumer
from fastapi import HTTPException
from app.core.db import get_db
from app.schema import order_pb2
from app.models.models import Order
from app.crud.crud import add_new_order, update_orders
# KAFKA_BROKER = "broker-1:19092,broker-2:19093,broker-3:19094"
# KAFKA_BROKER = "broker-1:19092"
KAFKA_TOPIC = "Orders"

async def consume_messages(topic=KAFKA_TOPIC):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers="broker-1:19092",
        group_id="orders_consumer",
        auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")

            order_data = json.loads(message.value)
            # new_todo.ParseFromString(message.value)
            order_key = message.key.decode()
            print(order_data)
            validated_data = Order.model_validate(order_data)
            print(validated_data)
            # inventory_data = json.loads(messag

            print(f"\n\n Consumer Deserialized data: {order_data }")
            with next(get_db()) as session:
                print("SAVING DATA TO DATABSE")
                if order_key == "Order Created":
                    print("sdsd")
                    db_insert_order =  add_new_order(
                        order_data=validated_data, session=session
                    )
                if order_key == "Order Updated": 
                    print("dsds")   
                    db_insert_order = update_orders(
                        data=validated_data, session=session
                    )
                    print("DB_INSERT_STOCK", db_insert_order)
            print("Done")

    except Exception as e:
        raise HTTPException(status_code=500, detail=(str(e)))
    finally:
        await consumer.stop()
