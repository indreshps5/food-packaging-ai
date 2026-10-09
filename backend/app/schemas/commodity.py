from pydantic import BaseModel


class FoodPropertiesResponse(BaseModel):
    moisture_content: float
    oil_fat_content: float
    pH: float
    respiration_rate: float


class CommodityResponse(BaseModel):
    id: int
    name: str
    category: str
    food_properties: FoodPropertiesResponse


class CommodityCreate(BaseModel):
    name: str
    category: str
    food_properties: dict