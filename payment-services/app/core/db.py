# import asyncio
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine
from . import settings


connection_string = str(settings.PAYMENT_DATABASE).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
