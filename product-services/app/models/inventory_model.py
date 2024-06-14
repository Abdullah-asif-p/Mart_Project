from sqlmodel import Field, SQLModel


class InventoryItem(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    product_id: str = Field(primary_key=True)
    name: str 
    quantity: int
    status: str = Field(default="Not Available")
