from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.application.use_cases.compare_packaging import (
    ComparePackagingUseCase,
)
from app.domain.value_objects.food_properties import FoodProperties
from app.domain.value_objects.storage_conditions import StorageConditions
from app.infrastructure.database.repositories.commodity_repository_impl import (
    CommodityRepositoryImpl,
)
from app.infrastructure.database.repositories.packaging_repository_impl import (
    PackagingRepositoryImpl,
)
from app.schemas.recommendation import RecommendationRequest


router = APIRouter(
    prefix="/compare",
    tags=["Packaging Comparison"],
)


@router.post("/")
def compare_packaging(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    commodity_repository = CommodityRepositoryImpl(db)
    packaging_repository = PackagingRepositoryImpl(db)

    commodity = commodity_repository.get_by_id(
        request.commodity_id
    )

    if commodity is None:
        raise HTTPException(
            status_code=404,
            detail="Commodity not found",
        )

    commodity.food_properties = FoodProperties(
        moisture_content=request.food_properties.moisture_content,
        oil_fat_content=request.food_properties.oil_fat_content,
        pH=request.food_properties.pH,
        respiration_rate=request.food_properties.respiration_rate,
    )

    storage_conditions = StorageConditions(
        temperature=request.storage_conditions.temperature,
        humidity=request.storage_conditions.humidity,
        storage_duration=request.storage_conditions.storage_duration,
        transportation_type=request.storage_conditions.transportation_type,
    )

    packaging_materials = packaging_repository.get_all()

    use_case = ComparePackagingUseCase()

    result = use_case.execute(
        commodity=commodity,
        packaging_materials=packaging_materials,
        storage_conditions=storage_conditions,
    )

    return result