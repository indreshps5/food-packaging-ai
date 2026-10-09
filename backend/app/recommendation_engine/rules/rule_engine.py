from typing import List

from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions

from app.recommendation_engine.rules.base_rule import PackagingRule
from app.recommendation_engine.rules.moisture_rule import MoistureRule
from app.recommendation_engine.rules.oxygen_rule import OxygenRule
from app.recommendation_engine.rules.temperature_rule import TemperatureRule
from app.recommendation_engine.rules.fat_compatibility_rule import (
    FatCompatibilityRule,
)
from app.recommendation_engine.rules.light_rule import LightRule


class ScientificRuleEngine:

    def __init__(self):
        self.rules: List[PackagingRule] = [
            MoistureRule(),
            OxygenRule(),
            TemperatureRule(),
            FatCompatibilityRule(),
            LightRule(),
        ]

    def filter_candidates(
        self,
        commodity: Commodity,
        packaging_materials: List[PackagingMaterial],
        storage_conditions: StorageConditions,
    ) -> List[PackagingMaterial]:

        valid_candidates = []

        for packaging in packaging_materials:
            is_valid = all(
                rule.evaluate(
                    commodity,
                    packaging,
                    storage_conditions,
                )
                for rule in self.rules
            )

            if is_valid:
                valid_candidates.append(packaging)

        return valid_candidates