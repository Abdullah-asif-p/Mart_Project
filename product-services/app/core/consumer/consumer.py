from aiokafka import AIOKafkaConsumer
from fastapi import HTTPException
from sqlmodel import select
from app.models.models import Product, ProductRating
from app.schema import product_schema_pb2
from app.core.db import get_db

KAFKA_BROKER = "broker-1:19092,broker-2:19093,broker-3:19094"
KAFKA_TOPIC = "Product"
# KAFKA_CONSUMER_GROUP_ID = "kafkafast-container"

async def consume_messages(topic:str=KAFKA_TOPIC):
    # Create a consumer instance.
    consumer1 = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id="my-group12",
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
            product_dict = {
                field.name: getattr(new_product, field.name)
                for field in new_product.DESCRIPTOR.fields
            }
            key = message.key.decode("utf-8")
            productratingvalidation = ProductRating.model_validate(product_dict['ratings'])
            product_dict['ratings'] = productratingvalidation
            product = Product(**product_dict)
            print(f"\n\n Consumer Deserialized data: {product}")
            print(f"\n\n Consumer : {new_product}")
            with next(get_db()) as session:
                get_product = session.exec(
                    select(Product).where(Product.id == product.id)
                ).first()
                # print("guyg7ug",product)
                if key == "Created" :
                    session.add(product)
                    session.commit()
                    session.refresh(product)
                    print("guyg7ug")
                elif key == "Deleted":
                    pass
                elif key == "Updated":
                    hero_data = product.model_dump(exclude_unset=True)
                    get_product.sqlmodel_update(hero_data)
                    session.add(get_product)
                    session.commit()
                    session.refresh(get_product)
                    print("g")
            print("Done")
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=(str(e)))
    finally:
        await consumer1.stop()
