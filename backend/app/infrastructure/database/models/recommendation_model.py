from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.infrastructure.database.connection import Base


class RecommendationModel(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    commodity_id = Column(
        Integer,
        ForeignKey("commodities.id"),
        nullable=False,
    )

    recommended_material_id = Column(
        Integer,
        ForeignKey("packaging_materials.id"),
        nullable=False,
    )

    scores = Column(JSONB, nullable=False)

    shelf_life = Column(JSONB, nullable=False)

    alternatives = Column(JSONB, nullable=False)

    explanation = Column(Text, nullable=False)