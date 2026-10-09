from app.domain.entities.commodity import Commodity
from app.domain.entities.packaging_material import PackagingMaterial

from app.domain.value_objects.food_properties import FoodProperties
from app.domain.value_objects.packaging_properties import PackagingProperties
from app.domain.value_objects.storage_conditions import StorageConditions

from app.recommendation_engine.rules.rule_engine import ScientificRuleEngine


commodity = Commodity(
    id=1,
    name="Rice",
    category="Grain",
    food_properties=FoodProperties(
        moisture_content=12.0,
        oil_fat_content=1.0,
        pH=6.5,
        respiration_rate=2.0,
    ),
)


packaging = PackagingMaterial(
    id=1,
    name="LDPE",
    material_type="Plastic",
    structure="Low-density polyethylene film",
    thickness=50.0,
    packaging_properties=PackagingProperties(
        oxygen_barrier=3,
        moisture_barrier=9,
        light_barrier=2,
        flexibility=9,
        sustainability_score=5,
    ),
)


storage_conditions = StorageConditions(
    temperature=25.0,
    humidity=50.0,
    storage_duration=90,
    transportation_type="Road",
)


rule_engine = ScientificRuleEngine()


result = rule_engine.filter_candidates(
    commodity=commodity,
    packaging_materials=[packaging],
    storage_conditions=storage_conditions,
)


print("Valid candidates:")
print(result)