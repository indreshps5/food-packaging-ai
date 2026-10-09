from sqlalchemy.orm import Session

from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.interfaces.packaging_repository import PackagingRepository
from app.infrastructure.database.mappers import packaging_model_to_domain
from app.infrastructure.database.models.packaging_model import PackagingModel


class PackagingRepositoryImpl(PackagingRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[PackagingMaterial]:
        models = (
            self.db
            .query(PackagingModel)
            .all()
        )

        return [
            packaging_model_to_domain(model)
            for model in models
        ]

    def get_by_id(
        self,
        packaging_id: int,
    ) -> PackagingMaterial | None:

        model = (
            self.db
            .query(PackagingModel)
            .filter(PackagingModel.id == packaging_id)
            .first()
        )

        if model is None:
            return None

        return packaging_model_to_domain(model)

    def get_by_name(
        self,
        name: str,
    ) -> PackagingMaterial | None:

        model = (
            self.db
            .query(PackagingModel)
            .filter(PackagingModel.name == name)
            .first()
        )

        if model is None:
            return None

        return packaging_model_to_domain(model)

    def create(
        self,
        name: str,
        material_type: str,
        structure: str,
        thickness: float,
        packaging_properties: dict,
    ) -> PackagingMaterial:

        packaging = PackagingModel(
            name=name,
            material_type=material_type,
            structure=structure,
            thickness=thickness,
            packaging_properties=packaging_properties,
        )

        self.db.add(packaging)
        self.db.commit()
        self.db.refresh(packaging)

        return packaging_model_to_domain(packaging)