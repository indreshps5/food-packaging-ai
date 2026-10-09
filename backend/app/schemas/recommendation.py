from pydantic import BaseModel, Field


class FoodPropertiesInput(BaseModel):
    moisture_content: float = Field(..., ge=0)
    oil_fat_content: float = Field(..., ge=0)
    pH: float
    respiration_rate: float = Field(..., ge=0)


class StorageConditionsInput(BaseModel):
    temperature: float
    humidity: float = Field(..., ge=0, le=100)
    storage_duration: int = Field(..., gt=0)
    transportation_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )


class RecommendationRequest(BaseModel):
    commodity_id: int = Field(..., gt=0)

    food_properties: FoodPropertiesInput

    storage_conditions: StorageConditionsInput