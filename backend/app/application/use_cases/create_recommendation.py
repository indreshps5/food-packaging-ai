from app.domain.value_objects.food_properties import FoodProperties
from app.domain.value_objects.storage_conditions import StorageConditions
from app.recommendation_engine.rules.rule_engine import ScientificRuleEngine
from app.recommendation_engine.optimization.scorer import PackagingScorer
from app.recommendation_engine.optimization.ranker import PackagingRanker
from app.recommendation_engine.optimization.shelf_life_estimator import (
    ShelfLifeEstimator,
)
from app.recommendation_engine.explanation.explanation_generator import (
    ExplanationGenerator,
)


class CreateRecommendationUseCase:
    def __init__(
        self,
        commodity_repository,
        packaging_repository,
        recommendation_repository,
    ):
        self.commodity_repository = commodity_repository
        self.packaging_repository = packaging_repository
        self.recommendation_repository = recommendation_repository

        self.rule_engine = ScientificRuleEngine()
        self.scorer = PackagingScorer()
        self.ranker = PackagingRanker(self.scorer)
        self.shelf_life_estimator = ShelfLifeEstimator()
        self.explanation_generator = ExplanationGenerator()

    def execute(
        self,
        user_id: int,
        commodity_id: int,
        food_properties_data: dict,
        storage_conditions_data: dict,
    ):
        commodity = self.commodity_repository.get_by_id(commodity_id)

        if commodity is None:
            return {
                "status": "not_found",
                "message": "Commodity not found.",
            }

        food_properties = FoodProperties(
            moisture_content=food_properties_data["moisture_content"],
            oil_fat_content=food_properties_data["oil_fat_content"],
            pH=food_properties_data["pH"],
            respiration_rate=food_properties_data["respiration_rate"],
        )

        storage_conditions = StorageConditions(
            temperature=storage_conditions_data["temperature"],
            humidity=storage_conditions_data["humidity"],
            storage_duration=storage_conditions_data["storage_duration"],
            transportation_type=storage_conditions_data["transportation_type"],
        )

        commodity.food_properties = food_properties

        packaging_materials = self.packaging_repository.get_all()

        valid_candidates = self.rule_engine.filter_candidates(
            commodity,
            packaging_materials,
            storage_conditions,
        )

        if not valid_candidates:
            return {
                "status": "no_suitable_packaging",
                "message": "No suitable packaging material found.",
            }

        ranked_candidates = self.ranker.rank(
            commodity,
            valid_candidates,
        )

        enriched_candidates = []

        for item in ranked_candidates:
            packaging = item["packaging"]
            scores = item["scores"]

            shelf_life = self.shelf_life_estimator.estimate(
                commodity,
                packaging,
                storage_conditions,
            )

            explanation = self.explanation_generator.generate(
                commodity,
                packaging,
                storage_conditions,
                scores,
                shelf_life,
            )

            enriched_candidates.append(
                {
                    "packaging": packaging,
                    "scores": scores,
                    "shelf_life": shelf_life,
                    "explanation": explanation,
                }
            )

        best_candidate = enriched_candidates[0]
        alternative_candidates = enriched_candidates[1:]

        alternatives_for_database = [
            {
                "packaging_id": item["packaging"].id,
                "name": item["packaging"].name,
                "material_type": item["packaging"].material_type,
                "overall_score": item["scores"]["overall_score"],
            }
            for item in alternative_candidates
        ]
        recommendation = self.recommendation_repository.create(
            user_id=user_id,
            commodity_id=commodity.id,
            recommended_material_id=best_candidate["packaging"].id,
            scores=best_candidate["scores"],
            shelf_life=best_candidate["shelf_life"],
            alternatives=alternatives_for_database,
            explanation=best_candidate["explanation"],
        )

        return {
            "status": "success",
            "recommendation_id": recommendation.id,
            "recommendation": best_candidate,
            "alternatives": alternative_candidates,
        }