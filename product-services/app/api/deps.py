from typing import Annotated, Any

from aiokafka import AIOKafkaProducer
from fastapi import Depends
from sqlmodel import Session
from core.db import get_db
from core.auth import get_user_dep
from core.producer.producer import get_producer


db_dependecy = Annotated[Session, Depends(get_db)]
AdminDep = Annotated[Any, Depends(get_user_dep)]
getproducer = Annotated[AIOKafkaProducer, Depends(get_producer)]
