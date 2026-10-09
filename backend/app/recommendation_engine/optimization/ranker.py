from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.recommendation_engine.optimization.scorer import PackagingScorer


class PackagingRanker:

    def __init__(
        self,
        scorer: PackagingScorer | None = None,
    ):
        self.scorer = scorer or PackagingScorer()

    def rank(
        self,
        commodity: Commodity,
        packaging_materials: list[PackagingMaterial],
    ) -> list[dict]:

        ranked_materials = []

        for packaging in packaging_materials:

            scores = self.scorer.calculate_scores(
                commodity,
                packaging,
            )

            ranked_materials.append(
                {
                    "packaging": packaging,
                    "scores": scores,
                }
            )

        ranked_materials.sort(
            key=lambda item: item["scores"]["overall_score"],
            reverse=True,
        )

        return ranked_materials