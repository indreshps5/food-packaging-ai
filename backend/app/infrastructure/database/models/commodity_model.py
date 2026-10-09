from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class CommodityModel(Base):
    __tablename__ = "commodities"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    food_properties: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )