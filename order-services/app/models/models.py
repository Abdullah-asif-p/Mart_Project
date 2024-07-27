from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import ARRAY, JSON, Column, Integer, Sequence, String
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4
from datetime import datetime, timezone


class Status(str, Enum):
    Pending = "pending"
    Completed = "completed"
    Progress = "in progress"


class Order(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str
    product_id: str 
    quantity:int 
    total_amount: float 
    status: Status = Field(default=Status.Pending.value)
    created_at: datetime = Field(default_factory=datetime.utcnow,)


class OrderCreate(SQLModel):
    product_id: str
    total_amount: float
    status: Status = Status.Pending.value
    quantity: int 

class OrderUpdate(SQLModel):
    product_id: str|None = None
    total_amount: float|None|None= None
    status: Status|None = None
    quantity: int|None = None


# class Status(Enum):
#     Pending = "pending"
#     Completed = "completed"


# class Order(SQLModel, table=True):
# id: str = Field(primary_key=True, index=True)
# user_id: str
# products: list["OrderItem"] = Relationship(back_populates="owner")
# total_amount: float
# status: Status = Field(default=Status.Pending.value)


# class OrderItem(SQLModel, table=True):
#     id: str = Field(default=None, primary_key=True)
#     order_id: str = Field(default=None, foreign_key="order.id")
#     product_id: str
#     owner: Order = Relationship(back_populates="products")


# class OrderDetails(BaseModel):
#     product_ids: list[str]
#     price: list[float]
# Data to save in the database
