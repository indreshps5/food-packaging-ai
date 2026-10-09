from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions


class ExplanationGenerator:

    def generate(
        self,
        commodity: Commodity,
        packaging: PackagingMaterial,
        storage_conditions: StorageConditions,
        scores: dict,
        shelf_life: dict,
    ) -> str:

        properties = packaging.packaging_properties
        food = commodity.food_properties

        reasons = []

        if properties.moisture_barrier >= 8:
            reasons.append("strong moisture protection")

        if properties.oxygen_barrier >= 8:
            reasons.append("strong oxygen protection")

        if properties.light_barrier >= 8:
            reasons.append("strong light protection")

        if properties.flexibility >= 7:
            reasons.append("good packaging flexibility")

        if food.moisture_content >= 70:
            reasons.append("suitable protection for a high-moisture commodity")

        if food.oil_fat_content >= 30:
            reasons.append("good compatibility with high-fat food")

        if storage_conditions.storage_duration >= 90:
            reasons.append("suitable for long-duration storage")

        if not reasons:
            reasons.append("acceptable overall packaging performance")

        reason_text = ", ".join(reasons)

        return (
            f"{packaging.name} is recommended for {commodity.name} "
            f"because it provides {reason_text}. "
            f"The packaging received an overall suitability score of "
            f"{scores['overall_score']}/10. "
            f"The estimated shelf life under the provided storage conditions "
            f"is {shelf_life['estimated_days']} days, compared with a "
            f"baseline estimate of {shelf_life['baseline_days']} days."
        )