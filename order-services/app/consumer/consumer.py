from aiokafka import AIOKafkaConsumer
from fastapi import HTTPException
from app.core.db import get_db
from app.schema import order_pb2
from app.models.models import Order
from app.crud.crud import add_new_order, update_orders
KAFKA_BROKER = "broker-1:19092,broker-2:19093,broker-3:19094"
KAFKA_TOPIC = "Orders"
# KAFKA_CONSUMER_GROUP_ID = "kafkafast-container"

async def consume_messages(topic=KAFKA_TOPIC):
    # Create a consumer instance.
    consumer1 = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id="orders_consumer",
        auto_offset_reset="earliest",
    )
    # consumer2 = AIOKafkaConsumer(
    #     "todos",
    #     bootstrap_servers="broker:19092",
    #     group_id="my-group",
    #     auto_offset_reset="earliest",
    #     enable_auto_commit=True,
    #     max_poll_records=10,  # Adjust based on throughput
    #     partition_assignment_strategy=["range"],
    #     group_instance_id="my-group-instance",  # Optional for consumer group rebalancing
    # )

    # Start the consumer.
    await consumer1.start()
    try:
        # Continuously listen for messages.
        async for message in consumer1:
            print(f"\n\n Consumer Raw message Vaue: {message.value}")
            
            new_todo = order_pb2.Order()
            new_todo.ParseFromString(message.value)
            order_key = message.key.decode()
            print(new_todo)
            validated_data = Order.model_validate(new_todo)
            print(validated_data)
            # inventory_data = json.loads(messag

            print(f"\n\n Consumer Deserialized data: {new_todo}")
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
                # if order_key == "Order Deleted" and orderid:
                #     print("SAVING DATA TO DATABSE")
                #     db_insert_order = delete_inventory_order_by_id(
                #         inventory_order_id=orderid, session=session
                #     )

            # session.add(new_todo)
            # session.commit()
            # session.refresh(Todo)
            print("Done")

    except Exception as e:
        raise HTTPException(status_code=500, detail=(str(e)))
    finally:
        await consumer1.stop()
