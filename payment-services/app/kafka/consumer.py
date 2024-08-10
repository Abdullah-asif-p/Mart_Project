import asyncio
from aiokafka import AIOKafkaConsumer
import json
import os
from app.crud.curd import create_payment_intent


async def consume_order_topic():
    consumer = AIOKafkaConsumer(
        "orders",
        bootstrap_servers="broker-1:19092",
        group_id="order-group",
        # value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )

    await consumer.start()
    await consumer.stop()
    try:
        async for message in consumer:
            order = message.value.decode("utf-8")
            product = order["product"]
            amount = order["amount"]
            # Call the function to create a Stripe payment intent
            payment_response = await create_payment_intent(amount)
            print(
                f"Processed order for product {product}: Payment intent created with response {payment_response}"
            )
    finally:
        await consumer.stop()
