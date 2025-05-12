from fastapi import APIRouter
from .endpoints import (
    auth,
    feedback,
    product,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
