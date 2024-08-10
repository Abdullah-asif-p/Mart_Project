from typing import Annotated, Any

from aiokafka import AIOKafkaProducer
from fastapi import Depends
from sqlmodel import Session
from app.core.db import get_db
from app.core.auth import get_user_dep
from app.kafka.producer import get_producer


db_dependency = Annotated[Session, Depends(get_db)]
AdminDep = Annotated[Any, Depends(get_user_dep)]
getproducer = Annotated[AIOKafkaProducer, Depends(get_producer)]
