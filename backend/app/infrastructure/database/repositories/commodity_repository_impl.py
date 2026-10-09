from sqlalchemy.orm import Session

from app.domain.entities.commodity import Commodity
from app.domain.interfaces.commodity_repository import CommodityRepository
from app.infrastructure.database.mappers import commodity_model_to_domain
from app.infrastructure.database.models.commodity_model import CommodityModel


class CommodityRepositoryImpl(CommodityRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Commodity]:
        models = (
            self.db
            .query(CommodityModel)
            .all()
        )

        return [
            commodity_model_to_domain(model)
            for model in models
        ]

    def get_by_id(
        self,
        commodity_id: int,
    ) -> Commodity | None:

        model = (
            self.db
            .query(CommodityModel)
            .filter(CommodityModel.id == commodity_id)
            .first()
        )

        if model is None:
            return None

        return commodity_model_to_domain(model)

    def get_by_name(
        self,
        name: str,
    ) -> Commodity | None:

        model = (
            self.db
            .query(CommodityModel)
            .filter(CommodityModel.name == name)
            .first()
        )

        if model is None:
            return None

        return commodity_model_to_domain(model)

    def create(
        self,
        name: str,
        category: str,
        food_properties: dict,
    ) -> Commodity:

        commodity = CommodityModel(
            name=name,
            category=category,
            food_properties=food_properties,
        )

        self.db.add(commodity)
        self.db.commit()
        self.db.refresh(commodity)

        return commodity_model_to_domain(commodity)