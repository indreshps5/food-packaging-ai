from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions


class MLEngine(ABC):

    @abstractmethod
    def predict(
        self,
        commodity: Commodity,
        packaging_materials: List[PackagingMaterial],
        storage_conditions: StorageConditions,
    ) -> List[float]:
        pass