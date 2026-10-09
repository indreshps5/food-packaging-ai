from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions

from app.recommendation_engine.rules.base_rule import PackagingRule


class TemperatureRule(PackagingRule):

    def evaluate(
        self,
        commodity: Commodity,
        packaging: PackagingMaterial,
        storage_conditions: StorageConditions,
    ) -> bool:

        temperature = storage_conditions.temperature
        material_type = packaging.material_type.lower()

        # Prototype rule:
        # very high-temperature storage should avoid
        # packaging materials with lower thermal suitability.
        if temperature >= 40:
            return material_type in {
                "metal",
                "glass",
            }

        return True