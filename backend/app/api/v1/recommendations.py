from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.application.use_cases.create_recommendation import (
    CreateRecommendationUseCase,
)
from app.infrastructure.database.repositories.commodity_repository_impl import (
    CommodityRepositoryImpl,
)
from app.infrastructure.database.repositories.packaging_repository_impl import (
    PackagingRepositoryImpl,
)
from app.infrastructure.database.repositories.recommendation_repository_impl import (
    RecommendationRepositoryImpl,
)
from app.schemas.recommendation import RecommendationRequest


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.post("/", status_code=status.HTTP_200_OK)
def create_recommendation(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    commodity_repository = CommodityRepositoryImpl(db)
    packaging_repository = PackagingRepositoryImpl(db)
    recommendation_repository = RecommendationRepositoryImpl(db)

    use_case = CreateRecommendationUseCase(
        commodity_repository=commodity_repository,
        packaging_repository=packaging_repository,
        recommendation_repository=recommendation_repository,
    )

    result = use_case.execute(
        user_id=current_user.id,
        commodity_id=request.commodity_id,
        food_properties_data=request.food_properties.model_dump(),
        storage_conditions_data=request.storage_conditions.model_dump(),
    )

    if result["status"] == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["message"],
        )

    if result["status"] == "no_suitable_packaging":
        return result

    best_candidate = result["recommendation"]
    alternatives = result["alternatives"]

    return {
        "status": result["status"],
        "recommendation_id": result["recommendation_id"],
        "user_id": current_user.id,
        "recommendation": {
            "packaging": {
                "id": best_candidate["packaging"].id,
                "name": best_candidate["packaging"].name,
                "material_type": best_candidate["packaging"].material_type,
                "structure": best_candidate["packaging"].structure,
                "thickness": best_candidate["packaging"].thickness,
            },
            "scores": best_candidate["scores"],
            "shelf_life": best_candidate["shelf_life"],
            "explanation": best_candidate["explanation"],
        },
        "alternatives": [
            {
                "packaging": {
                    "id": item["packaging"].id,
                    "name": item["packaging"].name,
                    "material_type": item["packaging"].material_type,
                    "structure": item["packaging"].structure,
                    "thickness": item["packaging"].thickness,
                },
                "scores": item["scores"],
            }
            for item in alternatives
        ],
    }