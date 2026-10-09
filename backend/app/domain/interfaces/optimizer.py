from abc import ABC, abstractmethod
from typing import List, Tuple

from app.domain.entities.packaging_material import PackagingMaterial


class Optimizer(ABC):

    @abstractmethod
    def rank(
        self,
        candidates: List[PackagingMaterial],
        ml_scores: List[float],
    ) -> List[Tuple[PackagingMaterial, float]]:
        pass