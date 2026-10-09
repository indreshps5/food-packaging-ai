from abc import ABC, abstractmethod
from typing import Any


class PackagingRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[Any]:
        pass

    @abstractmethod
    def get_by_id(self, packaging_id: int) -> Any | None:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Any | None:
        pass

    @abstractmethod
    def create(
        self,
        name: str,
        material_type: str,
        structure: str,
        thickness: float,
        packaging_properties: dict,
    ) -> Any:
        pass