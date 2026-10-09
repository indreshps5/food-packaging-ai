from dataclasses import dataclass

from app.domain.value_objects.packaging_properties import PackagingProperties


@dataclass
class PackagingMaterial:
    id: int
    name: str
    material_type: str
    structure: str
    thickness: float
    packaging_properties: PackagingProperties