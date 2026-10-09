from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions


class ShelfLifeEstimator:

    def estimate(
        self,
        commodity: Commodity,
        packaging: PackagingMaterial,
        storage_conditions: StorageConditions,
    ) -> dict:

        baseline_days = self._get_baseline_days(
            commodity
        )

        quality_factor = self._calculate_quality_factor(
            packaging
        )

        temperature_factor = self._calculate_temperature_factor(
            storage_conditions
        )

        humidity_factor = self._calculate_humidity_factor(
            storage_conditions
        )

        estimated_days = (
            baseline_days
            * quality_factor
            * temperature_factor
            * humidity_factor
        )

        estimated_days = max(
            1,
            round(estimated_days),
        )

        return {
            "estimated_days": estimated_days,
            "baseline_days": baseline_days,
        }

    def _get_baseline_days(
        self,
        commodity: Commodity,
    ) -> int:

        baseline_days = {
            "grain": 180,
            "oilseed": 150,
            "vegetable": 30,
            "fruit": 20,
        }

        category = commodity.category.lower()

        return baseline_days.get(
            category,
            30,
        )

    def _calculate_quality_factor(
        self,
        packaging: PackagingMaterial,
    ) -> float:

        properties = packaging.packaging_properties

        average_barrier = (
            properties.oxygen_barrier
            + properties.moisture_barrier
            + properties.light_barrier
        ) / 30

        return round(
            0.5 + average_barrier,
            2,
        )

    def _calculate_temperature_factor(
        self,
        storage_conditions: StorageConditions,
    ) -> float:

        temperature = storage_conditions.temperature

        if temperature <= 20:
            return 1.0

        if temperature <= 30:
            return 0.9

        if temperature <= 40:
            return 0.75

        return 0.6

    def _calculate_humidity_factor(
        self,
        storage_conditions: StorageConditions,
    ) -> float:

        humidity = storage_conditions.humidity

        if humidity <= 50:
            return 1.0

        if humidity <= 70:
            return 0.9

        if humidity <= 85:
            return 0.8

        return 0.7