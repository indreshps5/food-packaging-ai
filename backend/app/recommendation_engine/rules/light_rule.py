from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions

from app.recommendation_engine.rules.base_rule import PackagingRule


class LightRule(PackagingRule):

    def evaluate(
        self,
        commodity: Commodity,
        packaging: PackagingMaterial,
        storage_conditions: StorageConditions,
    ) -> bool:

        light_barrier = (
            packaging.packaging_properties.light_barrier
        )

        # Prototype rule:
        # Longer storage duration requires stronger
        # light protection.

        if storage_conditions.storage_duration >= 90:
            return light_barrier >= 2

        if storage_conditions.storage_duration >= 30:
            return light_barrier >= 2

        return light_barrier >= 1