from sqlalchemy.orm import Session

from app.infrastructure.database.models.recommendation_model import (
    RecommendationModel,
)


class RecommendationRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        commodity_id: int,
        recommended_material_id: int,
        scores: dict,
        shelf_life: dict,
        alternatives: list,
        explanation: str,
    ):
        recommendation = RecommendationModel(
            user_id=user_id,
            commodity_id=commodity_id,
            recommended_material_id=recommended_material_id,
            scores=scores,
            shelf_life=shelf_life,
            alternatives=alternatives,
            explanation=explanation,
        )

        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)

        return recommendation

    def get_by_id(self, recommendation_id: int):
        return (
            self.db.query(RecommendationModel)
            .filter(RecommendationModel.id == recommendation_id)
            .first()
        )

    def get_all(self):
        return self.db.query(RecommendationModel).all()

    def get_by_user_id(self, user_id: int):
        return (
            self.db.query(RecommendationModel)
            .filter(RecommendationModel.user_id == user_id)
            .order_by(RecommendationModel.id.desc())
            .all()
        )