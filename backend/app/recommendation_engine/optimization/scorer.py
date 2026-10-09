from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial


class PackagingScorer:

    def calculate_quality_score(
        self,
        commodity: Commodity,
        packaging: PackagingMaterial,
    ) -> float:

        properties = packaging.packaging_properties

        oxygen_score = properties.oxygen_barrier
        moisture_score = properties.moisture_barrier
        light_score = properties.light_barrier
        flexibility_score = properties.flexibility

        quality_score = (
            (oxygen_score * 0.30)
            + (moisture_score * 0.30)
            + (light_score * 0.20)
            + (flexibility_score * 0.20)
        )

        return round(quality_score, 2)

    def calculate_cost_score(
        self,
        packaging: PackagingMaterial,
    ) -> float:

        return round(
            packaging.packaging_properties.cost_score,
            2,
        )

    def calculate_sustainability_score(
        self,
        packaging: PackagingMaterial,
    ) -> float:

        return round(
            packaging.packaging_properties.sustainability_score,
            2,
        )

    def calculate_overall_score(
        self,
        quality_score: float,
        cost_score: float,
        sustainability_score: float,
    ) -> float:

        overall_score = (
            (quality_score * 0.50)
            + (cost_score * 0.20)
            + (sustainability_score * 0.30)
        )

        return round(overall_score, 2)

    def calculate_scores(
        self,
        commodity: Commodity,
        packaging: PackagingMaterial,
    ) -> dict:

        quality_score = self.calculate_quality_score(
            commodity,
            packaging,
        )

        cost_score = self.calculate_cost_score(
            packaging,
        )

        sustainability_score = self.calculate_sustainability_score(
            packaging,
        )

        overall_score = self.calculate_overall_score(
            quality_score,
            cost_score,
            sustainability_score,
        )

        return {
            "quality_score": quality_score,
            "cost_score": cost_score,
            "sustainability_score": sustainability_score,
            "overall_score": overall_score,
        }