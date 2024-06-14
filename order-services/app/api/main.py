from fastapi import APIRouter
from app.api.routes import routes

api_router = APIRouter()

api_router.include_router(routes.router, prefix="/order", tags=["order service"])
