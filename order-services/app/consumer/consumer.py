from aiokafka import AIOKafkaConsumer
from fastapi import HTTPException

from app.schema import order_pb2

KAFKA_BROKER = "broker:19092"
KAFKA_TOPIC = "todos"
# KAFKA_CONSUMER_GROUP_ID = "kafkafast-container"

async def consume_messages(topic=KAFKA_TOPIC):
    # Create a consumer instance.
    consumer1 = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id="order",
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

            print(f"\n\n Consumer Deserialized data: {new_todo}")
            # session.add(new_todo)
            # session.commit()
            # session.refresh(Todo)
            print("Done")

    except Exception as e:
        raise HTTPException(status_code=500, detail=(str(e)))
    finally:
        await consumer1.stop()
