from typing import List, Optional
import uuid
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, text
from uuid import UUID, uuid4


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
    ratings: "ProductRating" = Relationship(back_populates="product")


class ProductRating(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    product_id: str = Field(foreign_key="product.id")
    rating: int
    review: Optional[str] = None
    product: Optional[Product] = Relationship(back_populates="ratings")


# Define Pydantic models for request bodies and responses

# class ProductResponse(BaseModel):
#     id: str
#     name: str
#     description: str
#     price: float
#     category: str
#     stock: int
#     expiry: Optional[str]
#     brand: Optional[str]
#     weight: Optional[float]
#     sku: Optional[str]
#     ratings: List[ProductRatingResponse]

#     class Config:
#         from_attributes = True


class ProductRatingCreate(BaseModel):

    id: int| None
    rating: int
    review: Optional[str]


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    stock: int
    expiry: Optional[str] = None
    brand: Optional[str] = None
    weight: Optional[float] = None
    sku: Optional[str] = None
    ratings: ProductRatingCreate = None

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


# class ProductCreate(SQLModel):
#     name: str
#     description: str
#     price: float
#     category: str
#     stock: int


class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None
    stock: int | None = None
