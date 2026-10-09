from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.recommendation import Recommendation


class RecommendationRepository(ABC):

    @abstractmethod
    def get_by_id(
        self,
        recommendation_id: int
    ) -> Optional[Recommendation]:
        pass

    @abstractmethod
    def get_all(self) -> List[Recommendation]:
        pass

    @abstractmethod
    def save(
        self,
        recommendation: Recommendation
    ) -> Recommendation:
        pass