from sqlmodel import SQLModel, Field, Relationship


# Inventory Microservice Models
class InventoryItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: str
    name: str
    quantity: int
    status: str


class CreateInventoryItem(SQLModel):
    product_id: int
    name: str
    quantity: int
    status: str


class InventoryItemUpdate(SQLModel):
    quantity: int
    status: str = "Not Available"
