import json
from aiokafka import AIOKafkaConsumer
from app.core.db import get_db
from app.models.notification import Notifications
from app.crud import curd

ORDER_TOPIC = "orders"
KAFKA_BROKERS = "broker-1:19092"

async def consume_kafka_messages():
    """Consume messages from Kafka topics and process them based on topic."""

    # Initialize Kafka consumer
    consumer = AIOKafkaConsumer(
        ORDER_TOPIC,
        bootstrap_servers=KAFKA_BROKERS,
        auto_offset_reset="earliest",
        group_id="notification-service-1",
    )
    await consumer.start()

    try:
        # Consume messages from topics
        async for message in consumer:
            topic = message.topic
            value = message.value.decode("utf-8")

            try:
                if topic == ORDER_TOPIC:
                    order_data = json.loads(value)

                    print(order_data)
                    user_id = order_data["user_id"]
                    time = order_data["created_at"]
                    product_name = order_data["product_name"]
                    print(time)
                    print(product_name)

                    notification = Notifications(
                        message=f"Order {product_name} with status: {order_data['status']}.",
                        user_id=user_id,
                        time=time,
                    )
 
                    print(notification)

                    with next(get_db()) as session:
                        print("SAVING DATA TO DATABASE")
                        db_insert_product = curd.create_notification(
                            notifications=notification, db=session
                        )
                        print("db",db_insert_product)

            except Exception as e:
                print(f"Error processing message: {str(e)}")
 
    finally:
        await consumer.stop()
