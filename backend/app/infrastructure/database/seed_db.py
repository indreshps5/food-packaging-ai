from app.infrastructure.database.connection import SessionLocal

from app.infrastructure.database.models.commodity_model import CommodityModel
from app.infrastructure.database.models.packaging_model import PackagingModel


COMMODITIES = [
    {
        "name": "Rice",
        "category": "Grain",
        "food_properties": {
            "moisture_content": 12.0,
            "oil_fat_content": 1.0,
            "pH": 6.5,
            "respiration_rate": 2.0,
        },
    },
    {
        "name": "Wheat",
        "category": "Grain",
        "food_properties": {
            "moisture_content": 11.5,
            "oil_fat_content": 2.0,
            "pH": 6.2,
            "respiration_rate": 2.0,
        },
    },
    {
        "name": "Potato",
        "category": "Vegetable",
        "food_properties": {
            "moisture_content": 78.0,
            "oil_fat_content": 0.1,
            "pH": 5.5,
            "respiration_rate": 8.0,
        },
    },
    {
        "name": "Peanuts",
        "category": "Oilseed",
        "food_properties": {
            "moisture_content": 7.0,
            "oil_fat_content": 49.0,
            "pH": 6.0,
            "respiration_rate": 1.0,
        },
    },
    {
        "name": "Apple",
        "category": "Fruit",
        "food_properties": {
            "moisture_content": 84.0,
            "oil_fat_content": 0.2,
            "pH": 3.5,
            "respiration_rate": 12.0,
        },
    },
]


PACKAGING_MATERIALS = [
    {
        "name": "LDPE",
        "material_type": "Plastic",
        "structure": "Low-density polyethylene film",
        "thickness": 50,
        "packaging_properties": {
            "oxygen_barrier": 3,
            "moisture_barrier": 9,
            "light_barrier": 2,
            "flexibility": 9,
            "sustainability_score": 5,
            "cost_score": 8,
        },
    },
    {
        "name": "HDPE",
        "material_type": "Plastic",
        "structure": "High-density polyethylene film",
        "thickness": 50,
        "packaging_properties": {
            "oxygen_barrier": 5,
            "moisture_barrier": 9,
            "light_barrier": 4,
            "flexibility": 7,
            "sustainability_score": 5,
            "cost_score": 8,
        },
    },
    {
        "name": "PP",
        "material_type": "Plastic",
        "structure": "Polypropylene film",
        "thickness": 40,
        "packaging_properties": {
            "oxygen_barrier": 5,
            "moisture_barrier": 8,
            "light_barrier": 4,
            "flexibility": 8,
            "sustainability_score": 5,
            "cost_score": 8,
        },
    },
    {
        "name": "PET",
        "material_type": "Plastic",
        "structure": "Polyethylene terephthalate film",
        "thickness": 30,
        "packaging_properties": {
            "oxygen_barrier": 8,
            "moisture_barrier": 8,
            "light_barrier": 6,
            "flexibility": 5,
            "sustainability_score": 6,
            "cost_score": 6,
        },
    },
    {
        "name": "Paperboard",
        "material_type": "Paper",
        "structure": "Coated paperboard",
        "thickness": 300,
        "packaging_properties": {
            "oxygen_barrier": 4,
            "moisture_barrier": 5,
            "light_barrier": 8,
            "flexibility": 4,
            "sustainability_score": 8,
            "cost_score": 7,
        },
    },
    {
        "name": "Aluminium Foil",
        "material_type": "Metal",
        "structure": "Aluminium foil laminate",
        "thickness": 20,
        "packaging_properties": {
            "oxygen_barrier": 10,
            "moisture_barrier": 10,
            "light_barrier": 10,
            "flexibility": 6,
            "sustainability_score": 6,
            "cost_score": 4,
        },
    },
]


def seed_database() -> None:
    db = SessionLocal()
    try:
        # -----------------------------
        # Seed / update commodities
        # -----------------------------
        for data in COMMODITIES:
            existing = (
                db.query(CommodityModel)
                .filter(CommodityModel.name == data["name"])
                .first()
            )

            if existing is None:
                commodity = CommodityModel(
                    name=data["name"],
                    category=data["category"],
                    food_properties=data["food_properties"],
                )

                db.add(commodity)

            else:
                existing.category = data["category"]
                existing.food_properties = data["food_properties"]

        # -----------------------------
        # Seed / update packaging
        # -----------------------------
        for data in PACKAGING_MATERIALS:
            existing = (
                db.query(PackagingModel)
                .filter(PackagingModel.name == data["name"])
                .first()
            )

            if existing is None:
                packaging = PackagingModel(
                    name=data["name"],
                    material_type=data["material_type"],
                    structure=data["structure"],
                    thickness=data["thickness"],
                    packaging_properties=data["packaging_properties"],
                )

                db.add(packaging)

            else:
                existing.material_type = data["material_type"]
                existing.structure = data["structure"]
                existing.thickness = data["thickness"]
                existing.packaging_properties = data["packaging_properties"]

        db.commit()

        print("Database seeded successfully.")
        print("Existing records were updated where necessary.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()