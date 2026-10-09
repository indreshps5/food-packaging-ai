from dataclasses import dataclass
from typing import List

from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial


@dataclass
class RecommendationScores:
    quality_score: float
    cost_score: float
    sustainability_score: float
    overall_score: float


@dataclass
class ShelfLife:
    estimated_days: int
    baseline_days: int


@dataclass
class Recommendation:
    recommendation_id: int
    commodity: Commodity
    recommended_material: PackagingMaterial
    scores: RecommendationScores
    shelf_life: ShelfLife
    alternatives: List[str]
    explanation: str