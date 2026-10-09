from app.infrastructure.database.connection import Base, engine

# Import all models so SQLAlchemy knows about them.
from app.infrastructure.database.models.commodity_model import CommodityModel
from app.infrastructure.database.models.packaging_model import PackagingModel
from app.infrastructure.database.models.recommendation_model import (
    RecommendationModel,
)
from app.infrastructure.database.models.user_model import UserModel


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")