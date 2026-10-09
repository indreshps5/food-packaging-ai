from dataclasses import dataclass

from app.domain.value_objects.food_properties import FoodProperties


@dataclass
class Commodity:
    id: int
    name: str
    category: str
    food_properties: FoodProperties