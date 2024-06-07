from pydantic import BaseModel
from sqlmodel import Field, SQLModel, text
from uuid import UUID, uuid4


# Data to save in the database
class Product(SQLModel, table=True):
    id: str = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    description: str
    price: float
    category: str
    stock: int


class ProductCreate(SQLModel):
    name: str
    description: str
    price: float
    category: str
    stock: int


class ProductUpdate(SQLModel):
    name: str|None 
    description: str | None
    price: str | None
    category: str | None
    stock: str | None
