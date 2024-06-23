from typing import Annotated
from aiokafka import AIOKafkaProducer

# from app.schema.schema_registry import protobuf_serializer
from fastapi import Depends


async def get_kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers="broker-1:19092,broker-2:19093,broker-3:19094",
        # value_serializer=lambda v: protobuf_serializer(v, None),
    )
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()


get_producer = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
