from fastapi import APIRouter

from app.api.v1 import (
    auth,
    commodities,
    packaging,
    recommendations,
    history,
    admin,
    compare,
)


api_router = APIRouter(
    prefix="/api/v1"
)


api_router.include_router(auth.router)
api_router.include_router(commodities.router)
api_router.include_router(packaging.router)
api_router.include_router(recommendations.router)
api_router.include_router(history.router)
api_router.include_router(admin.router)
api_router.include_router(compare.router)