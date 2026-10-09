from dataclasses import dataclass


@dataclass(frozen=True)
class FoodProperties:
    moisture_content: float
    oil_fat_content: float
    pH: float
    respiration_rate: float