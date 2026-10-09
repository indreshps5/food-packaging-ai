from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_admin
from app.infrastructure.database.repositories.commodity_repository_impl import (
    CommodityRepositoryImpl,
)
from app.schemas.commodity import CommodityCreate


router = APIRouter(
    prefix="/commodities",
    tags=["Commodities"],
)


@router.get("/")
def get_commodities(
    db: Session = Depends(get_db),
):
    repository = CommodityRepositoryImpl(db)

    commodities = repository.get_all()

    return [
        {
            "id": commodity.id,
            "name": commodity.name,
            "category": commodity.category,
            "food_properties": {
                "moisture_content": (
                    commodity.food_properties.moisture_content
                ),
                "oil_fat_content": (
                    commodity.food_properties.oil_fat_content
                ),
                "pH": commodity.food_properties.pH,
                "respiration_rate": (
                    commodity.food_properties.respiration_rate
                ),
            },
        }
        for commodity in commodities
    ]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_commodity(
    commodity_data: CommodityCreate,
    db: Session = Depends(get_db),
):
    repository = CommodityRepositoryImpl(db)

    try:
        commodity = repository.create(
            name=commodity_data.name,
            category=commodity_data.category,
            food_properties=commodity_data.food_properties,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A commodity with this name may already exist.",
        )

    return {
        "id": commodity.id,
        "name": commodity.name,
        "category": commodity.category,
        "food_properties": {
            "moisture_content": (
                commodity.food_properties.moisture_content
            ),
            "oil_fat_content": (
                commodity.food_properties.oil_fat_content
            ),
            "pH": commodity.food_properties.pH,
            "respiration_rate": (
                commodity.food_properties.respiration_rate
            ),
        },
    }