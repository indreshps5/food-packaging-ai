from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_admin
from app.infrastructure.database.repositories.commodity_repository_impl import (
    CommodityRepositoryImpl,
)
from app.infrastructure.database.repositories.packaging_repository_impl import (
    PackagingRepositoryImpl,
)
from app.schemas.commodity import CommodityCreate
from app.schemas.packaging import PackagingCreate


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],
)


@router.get("/")
def admin_status():
    return {
        "status": "success",
        "message": "Admin API is working",
    }


@router.get("/commodities")
def list_commodities(db: Session = Depends(get_db)):
    repository = CommodityRepositoryImpl(db)
    commodities = repository.get_all()

    result = []

    for item in commodities:
        result.append(
            {
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "food_properties": {
                    "moisture_content": item.food_properties.moisture_content,
                    "oil_fat_content": item.food_properties.oil_fat_content,
                    "pH": item.food_properties.pH,
                    "respiration_rate": item.food_properties.respiration_rate,
                },
            }
        )

    return {
        "count": len(result),
        "commodities": result,
    }


@router.post(
    "/commodities",
    status_code=status.HTTP_201_CREATED,
)
def add_commodity(
    request: CommodityCreate,
    db: Session = Depends(get_db),
):
    required = {
        "moisture_content",
        "oil_fat_content",
        "pH",
        "respiration_rate",
    }

    if not required.issubset(request.food_properties.keys()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "food_properties must contain moisture_content, "
                "oil_fat_content, pH, and respiration_rate."
            ),
        )

    repository = CommodityRepositoryImpl(db)

    try:
        commodity = repository.create(
            name=request.name,
            category=request.category,
            food_properties=request.food_properties,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A commodity with this name may already exist.",
        )

    return {
        "status": "success",
        "message": "Commodity created successfully.",
        "commodity": {
            "id": commodity.id,
            "name": commodity.name,
            "category": commodity.category,
        },
    }


@router.get("/packaging")
def list_packaging_materials(db: Session = Depends(get_db)):
    repository = PackagingRepositoryImpl(db)
    materials = repository.get_all()

    result = []

    for item in materials:
        result.append(
            {
                "id": item.id,
                "name": item.name,
                "material_type": item.material_type,
                "structure": item.structure,
                "thickness": item.thickness,
                "packaging_properties": {
                    "oxygen_barrier": (
                        item.packaging_properties.oxygen_barrier
                    ),
                    "moisture_barrier": (
                        item.packaging_properties.moisture_barrier
                    ),
                    "light_barrier": (
                        item.packaging_properties.light_barrier
                    ),
                    "flexibility": item.packaging_properties.flexibility,
                    "sustainability_score": (
                        item.packaging_properties.sustainability_score
                    ),
                    "cost_score": item.packaging_properties.cost_score,
                },
            }
        )
        return {
        "count": len(result),
        "packaging_materials": result,
    }


@router.post(
    "/packaging",
    status_code=status.HTTP_201_CREATED,
)
def add_packaging_material(
    request: PackagingCreate,
    db: Session = Depends(get_db),
):
    required = {
        "oxygen_barrier",
        "moisture_barrier",
        "light_barrier",
        "flexibility",
        "sustainability_score",
        "cost_score",
    }

    if not required.issubset(request.packaging_properties.keys()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "packaging_properties must contain oxygen_barrier, "
                "moisture_barrier, light_barrier, flexibility, "
                "sustainability_score, and cost_score."
            ),
        )

    repository = PackagingRepositoryImpl(db)

    try:
        material = repository.create(
            name=request.name,
            material_type=request.material_type,
            structure=request.structure,
            thickness=request.thickness,
            packaging_properties=request.packaging_properties,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A packaging material with this name may already exist.",
        )

    return {
        "status": "success",
        "message": "Packaging material created successfully.",
        "packaging": {
            "id": material.id,
            "name": material.name,
            "material_type": material.material_type,
            "structure": material.structure,
            "thickness": material.thickness,
        },
    }