from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, text
from uuid import UUID, uuid4


# Data to save in the database
# class ProductRating(SQLModel, table=True):
#     id: str | None = Field(default=None, primary_key=True)
#     product_id: str = Field(foreign_key="product.id")
#     rating: int
#     review: str | None = None
#     product: "Product" = Relationship(back_populates="ratings")


# class Product(SQLModel, table=True):
#     id: str = Field(default_factory=uuid4, primary_key=True, index=True)
#     name: str
#     description: str
#     price: float
#     category: str
#     stock: int
#     expiry: str | None = None
#     brand: str | None = None
#     weight: float | None = None
#     sku: str | None = None
#     rating: List["ProductRating"] = Relationship(back_populates="product")


class Product(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    name: str
    description: str
    price: float
    category: str
    stock: int
    expiry: Optional[str] = None
    brand: Optional[str] = None
    weight: Optional[float] = None
    sku: Optional[str] = None
    ratings: List["ProductRating"] = Relationship(back_populates="product")


class ProductRating(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    product_id: str = Field(foreign_key="product.id")
    rating: int
    review: Optional[str] = None
    product: Optional[Product] = Relationship( back_populates="ratings")


# class Team(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     headquarters: str

#     heroes: list["Hero"] = Relationship()


# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     secret_name: str
#     age: int | None = Field(default=None, index=True)

#     team_id: int | None = Field(default=None, foreign_key="team.id")
#     team: Team | None = Relationship()


class ProductCreate(SQLModel):
    name: str
    description: str
    price: float
    category: str
    stock: int


class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None
    stock: int | None = None
