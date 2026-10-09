from abc import ABC, abstractmethod

from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial
from app.domain.value_objects.storage_conditions import StorageConditions


class PackagingRule(ABC):

    @abstractmethod
    def evaluate(
        self,
        commodity: Commodity,
        packaging: PackagingMaterial,
        storage_conditions: StorageConditions,
    ) -> bool:
        """
        Return True if the packaging material satisfies this rule.
        """
        pass