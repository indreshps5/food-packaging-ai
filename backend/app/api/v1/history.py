from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.repositories.recommendation_repository_impl import (
    RecommendationRepositoryImpl,
)


router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get("/")
def get_recommendation_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    recommendation_repository = RecommendationRepositoryImpl(db)

    recommendations = recommendation_repository.get_by_user_id(
        current_user.id
    )

    return {
        "count": len(recommendations),
        "user_id": current_user.id,
        "history": [
            {
                "recommendation_id": recommendation.id,
                "commodity_id": recommendation.commodity_id,
                "recommended_material_id": recommendation.recommended_material_id,
                "scores": recommendation.scores,
                "shelf_life": recommendation.shelf_life,
                "alternatives": recommendation.alternatives,
                "explanation": recommendation.explanation,
            }
            for recommendation in recommendations
        ],
    }


@router.get("/{recommendation_id}")
def get_recommendation_by_id(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    recommendation_repository = RecommendationRepositoryImpl(db)

    recommendation = recommendation_repository.get_by_id(
        recommendation_id
    )

    if (
        recommendation is None
        or recommendation.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found.",
        )

    return {
        "status": "success",
        "recommendation": {
            "recommendation_id": recommendation.id,
            "commodity_id": recommendation.commodity_id,
            "recommended_material_id": recommendation.recommended_material_id,
            "scores": recommendation.scores,
            "shelf_life": recommendation.shelf_life,
            "alternatives": recommendation.alternatives,
            "explanation": recommendation.explanation,
        },
    }