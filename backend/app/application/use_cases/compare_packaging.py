from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions
from app.recommendation_engine.rules.rule_engine import ScientificRuleEngine
from app.recommendation_engine.optimization.ranker import PackagingRanker


class ComparePackagingUseCase:

    def __init__(
        self,
        rule_engine=None,
        ranker=None,
    ):
        self.rule_engine = rule_engine or ScientificRuleEngine()
        self.ranker = ranker or PackagingRanker()

    def execute(
        self,
        commodity: Commodity,
        packaging_materials: list[PackagingMaterial],
        storage_conditions: StorageConditions,
    ):

        valid_candidates = self.rule_engine.filter_candidates(
            commodity=commodity,
            packaging_materials=packaging_materials,
            storage_conditions=storage_conditions,
        )

        if not valid_candidates:
            return {
                "status": "no_suitable_packaging",
                "message": (
                    "No packaging material satisfies "
                    "the current prototype rules."
                ),
                "comparisons": [],
            }

        ranked_candidates = self.ranker.rank(
            commodity=commodity,
            packaging_materials=valid_candidates,
        )

        comparisons = []

        for item in ranked_candidates:
            packaging = item["packaging"]

            comparisons.append(
                {
                    "packaging": {
                        "id": packaging.id,
                        "name": packaging.name,
                        "material_type": packaging.material_type,
                        "structure": packaging.structure,
                        "thickness": packaging.thickness,
                    },
                    "scores": item["scores"],
                }
            )

        return {
            "status": "success",
            "comparisons": comparisons,
        }