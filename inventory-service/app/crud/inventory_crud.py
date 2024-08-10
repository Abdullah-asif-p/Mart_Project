import json
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import (
    CreateInventoryItem,
    InventoryItem,
    InventoryItemUpdate,
)
from app.schema import inventory_schema_pb2


# Add a New Inventory Item to the Database
def add_new_inventory_item(inventory_item_data: InventoryItem, session: Session):
    print("Adding Inventory Item to Database")
    data = InventoryItem.model_validate(inventory_item_data)
    print(data)
    session.add(data)
    session.commit()
    session.refresh(data)
    print(inventory_item_data)
    return data

def delete_inventory_item(inventory_item_data: InventoryItem, session: Session):
    print("Delete Inventory Item to Database")
    data = InventoryItem.model_validate(inventory_item_data)
    session.delete(data)
    session.commit()
    print(inventory_item_data)
    return data


# Get All Inventory Items from the Database
def get_all_inventory_items(session: Session):
    all_inventory_items = session.exec(select(InventoryItem)).all()
    return all_inventory_items

def get_all_active_inventory_items(session: Session):
    all_inventory_items = session.exec(select(InventoryItem).where(InventoryItem.status == "Available")).all()
    return all_inventory_items

# Get an Inventory Item by ID
def get_inventory_item_by_id(inventory_item_id: int, session: Session):
    inventory_item = session.exec(
        select(InventoryItem).where(InventoryItem.id == inventory_item_id)
    ).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory Item not found")
    return inventory_item


# Delete Inventory Item by ID
def delete_inventory_item_by_id(inventory_item_id: str, session: Session):
    # Step 1: Get the Inventory Item by ID
    inventory_item = session.exec(
        select(InventoryItem).where(InventoryItem.product_id == inventory_item_id)
    ).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory Item not found")
    # Step 2: Delete the Inventory Item
    session.delete(inventory_item)
    session.commit()
    return {"message": "Inventory Item Deleted Successfully"}


# # Update Product by ID
async def update_inventory_item(
    product_id: int, UpdateInventory: InventoryItemUpdate, session: Session, producer
):
    # Step 1: Get the Product by ID
    inventory_item = session.exec(
        select(InventoryItem).where(InventoryItem.id == product_id)
    ).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="inventory item not found")
    # Step 2: Update the Product
    hero_data = UpdateInventory.model_dump(exclude_unset=True)
    inventory_item.sqlmodel_update(hero_data)
    Inventorykey = ("Product Updated").encode("utf-8")

    inventory_dict = {
        field: getattr(inventory_item, field) for field in inventory_item.dict()
    }
    inventory_json = json.dumps(inventory_dict).encode("utf-8")
    # inventory_item_proto = inventory_schema_pb2.InventoryItem(
    #     id=inventory_item.id,
    #     product_id=inventory_item.product_id,
    #     name=inventory_item.name,
    #     quantity=inventory_item.quantity,
    #     status=inventory_item.status
    # )
    # print(inventory_item_proto)
    # serialized_product = inventory_item.SerializeToString()
    send_result = await producer.send_and_wait(
        "Initialise_Inventory", value=inventory_json, key=Inventorykey
    )
    print(f"send_result:{send_result}")
    session.add(inventory_item)
    session.commit()
    return inventory_item


async def update_inventory_product(
    product_id: str, UpdateInventory: InventoryItemUpdate, session: Session, producer
):
    # Step 1: Get the Product by ID
    inventory_item = session.exec(
        select(InventoryItem).where(InventoryItem.product_id == product_id)
    ).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="inventory item not found")
    # Step 2: Update the Product
    hero_data = UpdateInventory.model_dump(exclude_unset=True)
    inventory_item.sqlmodel_update(hero_data)
    Inventorykey = ("Product Updated").encode("utf-8")

    inventory_dict = {
        field: getattr(inventory_item, field) for field in inventory_item.dict()
    }
    print(inventory_dict)
    inventory_json = json.dumps(inventory_dict).encode("utf-8")
    # inventory_item_proto = inventory_schema_pb2.InventoryItem(
    #     id=(inventory_item.id),
    #     product_id=inventory_item.product_id,
    #     name=inventory_item.name,
    #     quantity=inventory_item.quantity,
    #     status=inventory_item.status
    # )
    # print(inventory_item_proto)
    # serialized_product = inventory_item.SerializeToString()
    if inventory_dict["quantity"] >= 1 and inventory_dict["status"] =="Available" :
        send_result1 = await producer.send_and_wait("Inventory", value=inventory_json, key=Inventorykey)
        print(send_result1)
    send_result = await producer.send_and_wait(
        "Initialise_Inventory", value=inventory_json, key=Inventorykey
    )
    print(f"send_result:{send_result}")
    session.add(inventory_item)
    session.commit()
    return inventory_item



# def update_inventory_item(
#     product_id: int, UpdateInventory: InventoryItemUpdate, session: Session, producer
# ):
#     # Step 1: Get the Product by ID
#     inventory_item = session.exec(
#         select(InventoryItem).where(InventoryItem.id == product_id)
#     ).one_or_none()
#     if inventory_item is None:
#         raise HTTPException(status_code=404, detail="inventory item not found")
#     # Step 2: Update the Product
#     hero_data = UpdateInventory.model_dump(exclude_unset=True)
#     inventory_item.sqlmodel_update(hero_data)
#     session.add(inventory_item)
#     session.commit()
#     return inventory_item
