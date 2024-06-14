import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from app.consumer.consumer import consume_messages
from app.api import main as router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    task = task = asyncio.create_task(consume_messages("order"))
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Order-mangement API",
    version="0.0.1",
    # servers=[{"url": "http://localhost:8000", "description": "Development server"}],
)

origins =["*"]

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
