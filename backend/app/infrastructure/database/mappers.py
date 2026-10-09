from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.food_properties import FoodProperties
from app.domain.value_objects.packaging_properties import PackagingProperties

from app.infrastructure.database.models.commodity_model import CommodityModel
from app.infrastructure.database.models.packaging_model import PackagingModel


def commodity_model_to_domain(
    model: CommodityModel,
) -> Commodity:
    # Handle missing or null food-property data safely.
    food_data = model.food_properties or {}

    food_properties = FoodProperties(
        moisture_content=food_data.get("moisture_content", 0.0),
        oil_fat_content=food_data.get("oil_fat_content", 0.0),
        pH=food_data.get("pH", 7.0),
        respiration_rate=food_data.get("respiration_rate", 0.0),
    )

    return Commodity(
        id=model.id,
        name=model.name,
        category=model.category,
        food_properties=food_properties,
    )


def packaging_model_to_domain(
    model: PackagingModel,
) -> PackagingMaterial:
    # Handle missing or null packaging-property data safely.
    packaging_data = model.packaging_properties or {}

    packaging_properties = PackagingProperties(
        oxygen_barrier=packaging_data.get("oxygen_barrier", 0.0),
        moisture_barrier=packaging_data.get("moisture_barrier", 0.0),
        light_barrier=packaging_data.get("light_barrier", 0.0),
        flexibility=packaging_data.get("flexibility", 0.0),
        sustainability_score=packaging_data.get(
            "sustainability_score", 0.0
        ),
        cost_score=packaging_data.get("cost_score", 0.0),
    )

    return PackagingMaterial(
        id=model.id,
        name=model.name,
        material_type=model.material_type,
        structure=model.structure,
        thickness=model.thickness,
        packaging_properties=packaging_properties,
    )