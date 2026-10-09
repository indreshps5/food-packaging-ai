from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions
from app.recommendation_engine.rules.rule_engine import ScientificRuleEngine
from app.recommendation_engine.optimization.ranker import PackagingRanker
from app.recommendation_engine.optimization.shelf_life_estimator import ShelfLifeEstimator
from app.recommendation_engine.explanation.explanation_generator import (
    ExplanationGenerator,
)


class RecommendationService:
    def __init__(
        self,
        rule_engine=None,
        ranker=None,
        shelf_life_estimator=None,
        explanation_generator=None,
    ):
        self.rule_engine = rule_engine or ScientificRuleEngine()
        self.ranker = ranker or PackagingRanker()
        self.shelf_life_estimator = (
            shelf_life_estimator or ShelfLifeEstimator()
        )
        self.explanation_generator = (
            explanation_generator or ExplanationGenerator()
        )

    def generate_recommendation(
        self,
        commodity,
        packaging_materials,
        storage_conditions,
    ):
        valid_candidates = self.rule_engine.filter_candidates(
            commodity=commodity,
            packaging_materials=packaging_materials,
            storage_conditions=storage_conditions,
        )

        if not valid_candidates:
            return {
                "status": "no_suitable_packaging",
                "message": "No packaging material satisfies the current prototype rules.",
                "recommendation": None,
                "alternatives": [],
            }

        ranked_candidates = self.ranker.rank(
            commodity=commodity,
            packaging_materials=valid_candidates,
        )

        best_candidate = ranked_candidates[0]

        shelf_life = self.shelf_life_estimator.estimate(
            commodity=commodity,
            packaging=best_candidate["packaging"],
            storage_conditions=storage_conditions,
        )

        explanation = self.explanation_generator.generate(
            commodity=commodity,
            packaging=best_candidate["packaging"],
            storage_conditions=storage_conditions,
            scores=best_candidate["scores"],
            shelf_life=shelf_life,
        )

        best_candidate["shelf_life"] = shelf_life
        best_candidate["explanation"] = explanation

        alternatives = ranked_candidates[1:]

        return {
            "status": "success",
            "recommendation": best_candidate,
            "alternatives": alternatives,
        }