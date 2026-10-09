from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions


class RuleEngine(ABC):

    @abstractmethod
    def filter_candidates(
        self,
        commodity: Commodity,
        packaging_materials: List[PackagingMaterial],
        storage_conditions: StorageConditions,
    ) -> List[PackagingMaterial]:
        pass