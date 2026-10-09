from pydantic import BaseModel, Field


class PackagingPropertiesResponse(BaseModel):
    oxygen_barrier: float
    moisture_barrier: float
    light_barrier: float
    flexibility: float
    sustainability_score: float
    cost_score: float


class PackagingResponse(BaseModel):
    id: int
    name: str
    material_type: str
    structure: str
    thickness: float
    packaging_properties: PackagingPropertiesResponse


class PackagingCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    material_type: str = Field(..., min_length=1, max_length=100)
    structure: str = Field(..., min_length=1, max_length=150)
    thickness: float = Field(..., gt=0)
    packaging_properties: dict