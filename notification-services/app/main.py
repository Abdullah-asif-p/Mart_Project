# import asyncio

import asyncio
from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from app.api import main as router
from app.kafka.consumer import consume_kafka_messages

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating table...")

    task = asyncio.create_task(consume_kafka_messages())
    create_db_and_tables()
    print("\n\n LIFESPAN created!! \n\n")
    yield


app = FastAPI(
    lifespan=lifespan,
    title="notifications ",
    version="0.0.1",
    # servers=[{"url": "http://localhost:8000", "description": "Development server"}],
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router.api_router)
# app.include_router(router, prefix="/product")
