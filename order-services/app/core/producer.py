from aiokafka import AIOKafkaProducer
from app.schema.schema_registry import protobuf_serializer

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
