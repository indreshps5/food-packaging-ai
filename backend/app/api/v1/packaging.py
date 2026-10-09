from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.infrastructure.database.repositories.packaging_repository_impl import (
    PackagingRepositoryImpl,
)
from app.schemas.packaging import PackagingCreate


router = APIRouter(
    prefix="/packaging",
    tags=["Packaging"],
)


@router.get("/")
def get_packaging_materials(
    db: Session = Depends(get_db),
):
    repository = PackagingRepositoryImpl(db)

    packaging_materials = repository.get_all()

    return [
        {
            "id": packaging.id,
            "name": packaging.name,
            "material_type": packaging.material_type,
            "structure": packaging.structure,
            "thickness": packaging.thickness,
            "packaging_properties": {
                "oxygen_barrier": (
                    packaging.packaging_properties.oxygen_barrier
                ),
                "moisture_barrier": (
                    packaging.packaging_properties.moisture_barrier
                ),
                "light_barrier": (
                    packaging.packaging_properties.light_barrier
                ),
                "flexibility": (
                    packaging.packaging_properties.flexibility
                ),
                "sustainability_score": (
                    packaging.packaging_properties.sustainability_score
                ),
                "cost_score": (
                    packaging.packaging_properties.cost_score
                ),
            },
        }
        for packaging in packaging_materials
    ]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_packaging_material(
    packaging_data: PackagingCreate,
    db: Session = Depends(get_db),
):
    repository = PackagingRepositoryImpl(db)

    packaging = repository.create(
        name=packaging_data.name,
        material_type=packaging_data.material_type,
        structure=packaging_data.structure,
        thickness=packaging_data.thickness,
        packaging_properties=packaging_data.packaging_properties,
    )

    return {
        "id": packaging.id,
        "name": packaging.name,
        "material_type": packaging.material_type,
        "structure": packaging.structure,
        "thickness": packaging.thickness,
        "packaging_properties": {
            "oxygen_barrier": (
                packaging.packaging_properties.oxygen_barrier
            ),
            "moisture_barrier": (
                packaging.packaging_properties.moisture_barrier
            ),
            "light_barrier": (
                packaging.packaging_properties.light_barrier
            ),
            "flexibility": (
                packaging.packaging_properties.flexibility
            ),
            "sustainability_score": (
                packaging.packaging_properties.sustainability_score
            ),
            "cost_score": (
                packaging.packaging_properties.cost_score
            ),
        },
    }