from abc import ABC, abstractmethod
from typing import Any


class CommodityRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[Any]:
        pass

    @abstractmethod
    def get_by_id(self, commodity_id: int) -> Any | None:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Any | None:
        pass

    @abstractmethod
    def create(
        self,
        name: str,
        category: str,
        food_properties: dict,
    ) -> Any:
        pass