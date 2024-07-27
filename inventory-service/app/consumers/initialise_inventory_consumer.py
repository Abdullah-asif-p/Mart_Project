from aiokafka import AIOKafkaConsumer
import json
from app.core.db import get_db
from app.crud.inventory_crud import add_new_inventory_item, delete_inventory_item, delete_inventory_item_by_id
from app.models.inventory_model import InventoryItem
from app.schema import inventory_schema_pb2

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
            new_product = inventory_schema_pb2.Intailise_Inventory()
            new_product.ParseFromString(message.value)

            # inventory_data = json.loads(message.value.decode())
            inventory_key = message.key.decode()
            print(inventory_key)
            print("TYPE", (type(new_product)))
            print(f"Inventory Data {new_product}")
            productid= new_product.product_id
            print(productid)
            with next(get_db()) as session:
                print("SAVING DATA TO DATABSE")
                if inventory_key == "Product Created":
                    inventory_data=InventoryItem(
                    product_id= new_product.product_id,
                    name= new_product.name,
                    quantity= 0,
                    status= new_product.status
                  )
                    validated_data= InventoryItem.model_validate(inventory_data)
                    db_insert_product = add_new_inventory_item(
                        inventory_item_data=validated_data, session=session
                    )
                if inventory_key == "Product Deleted" and productid:
                    print("SAVING DATA TO DATABSE")
                    db_insert_product = delete_inventory_item_by_id(
                        inventory_item_id=productid, session=session
                    )
                print("DB_INSERT_STOCK", db_insert_product)

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
