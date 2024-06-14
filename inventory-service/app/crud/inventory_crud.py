from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import CreateInventoryItem, InventoryItem, InventoryItemUpdate


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


# Get All Inventory Items from the Database
def get_all_inventory_items(session: Session):
    all_inventory_items = session.exec(select(InventoryItem)).all()
    return all_inventory_items

# Get an Inventory Item by ID
def get_inventory_item_by_id(inventory_item_id: int, session: Session):
    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory Item not found")
    return inventory_item

# Delete Inventory Item by ID
def delete_inventory_item_by_id(inventory_item_id: int, session: Session):
    # Step 1: Get the Inventory Item by ID
    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory Item not found")
    # Step 2: Delete the Inventory Item
    session.delete(inventory_item)
    session.commit()
    return {"message": "Inventory Item Deleted Successfully"}


# # Update Product by ID
def update_inventory_item(
    product_id: int, UpdateInventory: InventoryItemUpdate, session: Session
):
    # Step 1: Get the Product by ID
    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == product_id)).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="inventory item not found")
    # Step 2: Update the Product
    hero_data = UpdateInventory.model_dump(exclude_unset=True)
    inventory_item.sqlmodel_update(hero_data)
    session.add(inventory_item)
    session.commit()
    return inventory_item 
