from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions

from app.recommendation_engine.rules.base_rule import PackagingRule


class FatCompatibilityRule(PackagingRule):

    def evaluate(
        self,
        commodity: Commodity,
        packaging: PackagingMaterial,
        storage_conditions: StorageConditions,
    ) -> bool:

        fat_content = commodity.food_properties.oil_fat_content
        material_type = packaging.material_type.lower()

        # Prototype compatibility rule for high-fat commodities.
        if fat_content >= 30:
            return material_type in {
                "metal",
                "plastic",
                "glass",
            }

        return True