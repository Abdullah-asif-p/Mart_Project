import json
from fastapi import APIRouter, HTTPException
from app.core.db import db_dependency
from app.models.inventory_model import InventoryItem, InventoryItemUpdate
from app.api.deps.producer import get_producer
from app.crud.inventory_crud import get_all_inventory_items, get_inventory_item_by_id,delete_inventory_item_by_id, update_inventory_item
router = APIRouter()

# @router.patch("/manage-inventory/", response_model=InventoryItem)
# async def create_new_inventory_item(
#     item: InventoryItem,
#     session: db_dependency,
#     producer: get_producer,
# ):
#     """Create a new inventory item and send it to Kafka"""

#     item_dict = {field: getattr(item, field) for field in item.dict()}
#     item_json = json.dumps(item_dict).encode("utf-8")
#     print("item_JSON:", item_json)
#     # Produce message
#     await producer.send_and_wait("AddStock", item_json)
#     # new_item = add_new_inventory_item(item, session)
#     return item


@router.get("/manage-inventory/all", response_model=list[InventoryItem])
def all_inventory_items(session: db_dependency):
    """Get all inventory items from the database"""
    return get_all_inventory_items(session)


@router.get("/manage-inventory/{item_id}", response_model=InventoryItem)
def single_inventory_item(
    item_id: int, session: db_dependency
):
    """Get a single inventory item by ID"""
    try:
        return get_inventory_item_by_id(inventory_item_id=item_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/manage-inventory/{item_id}", response_model=dict)
def delete_single_inventory_item(
    item_id: int, session: db_dependency
):
    """Delete a single inventory item by ID"""
    try:
        return delete_inventory_item_by_id(inventory_item_id=item_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/manage-inventory/{item_id}", response_model=InventoryItem)
def update_single_inventory_item(item_id: int, item: InventoryItemUpdate, session: db_dependency):
    """ Update a single inventory item by ID"""
    try:
        return update_inventory_item(
            product_id=item_id, UpdateInventory=item, session=session
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
