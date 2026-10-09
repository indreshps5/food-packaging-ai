from sqlalchemy import Integer, String, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class PackagingModel(Base):
    __tablename__ = "packaging_materials"

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

    material_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    structure: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    thickness: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    packaging_properties: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )