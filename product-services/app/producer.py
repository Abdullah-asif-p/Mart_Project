from typing import Annotated
from aiokafka import AIOKafkaProducer
from .schema_registry import protobuf_serializer
from fastapi import Depends

async def get_kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers="broker:19092",
        # value_serializer=lambda v: protobuf_serializer(v, None),
    )
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()


producer= Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
