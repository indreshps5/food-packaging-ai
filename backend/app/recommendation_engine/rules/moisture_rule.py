from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions

from app.recommendation_engine.rules.base_rule import PackagingRule


class MoistureRule(PackagingRule):

    def evaluate(
        self,
        commodity: Commodity,
        packaging: PackagingMaterial,
        storage_conditions: StorageConditions,
    ) -> bool:

        moisture = commodity.food_properties.moisture_content
        moisture_barrier = (
            packaging.packaging_properties.moisture_barrier
        )

        # High-moisture commodities require stronger
        # moisture-barrier packaging.
        if moisture >= 70:
            return moisture_barrier >= 7

        if moisture >= 30:
            return moisture_barrier >= 5

        return moisture_barrier >= 3