from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions

from app.recommendation_engine.rules.base_rule import PackagingRule


class OxygenRule(PackagingRule):

    def evaluate(
        self,
        commodity: Commodity,
        packaging: PackagingMaterial,
        storage_conditions: StorageConditions,
    ) -> bool:

        fat_content = commodity.food_properties.oil_fat_content
        oxygen_barrier = (
            packaging.packaging_properties.oxygen_barrier
        )

        # Higher-fat foods are more sensitive to oxidation.
        if fat_content >= 20:
            return oxygen_barrier >= 8

        if fat_content >= 5:
            return oxygen_barrier >= 6

        return oxygen_barrier >= 3