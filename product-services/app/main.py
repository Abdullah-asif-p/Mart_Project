import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from .routes import router 
from .consumer import consume_messages

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    asyncio.create_task(consume_messages())
    create_db_and_tables()
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Product-mangement API",
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



app.include_router(router, prefix="/product")
