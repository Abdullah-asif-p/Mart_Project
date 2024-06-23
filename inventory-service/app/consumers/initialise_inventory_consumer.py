from aiokafka import AIOKafkaConsumer
import json
from app.core.db import get_db
from app.crud.inventory_crud import add_new_inventory_item
from app.models.inventory_model import InventoryItem

async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="invt",
        auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("RAW ADD STOCK CONSUMER MESSAGE")
            print(f"Received message on topic {message.topic}")

            inventory_data = json.loads(message.value.decode())
            inventory_key = message.key.decode()
            print(inventory_key)
            print("TYPE", (type(inventory_data)))
            print(f"Inventory Data {inventory_data}")
            
            with next(get_db()) as session:
                print("SAVING DATA TO DATABSE")
                validated_data= InventoryItem.model_validate(inventory_data)
                if inventory_key == "Product Created":
                    db_insert_product = add_new_inventory_item(
                        inventory_item_data=validated_data, session=session
                    )
                elif inventory_key == "Product Updated":
                    pass

                print("DB_INSERT_STOCK", db_insert_product)

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
