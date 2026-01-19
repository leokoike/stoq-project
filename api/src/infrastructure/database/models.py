from datetime import datetime
import uuid

from sqlalchemy import UUID, Boolean, DateTime, Enum, Float, String, LargeBinary
from src.domain.entities.product import SellingPlaceEnum
from src.infrastructure.database.connection import Base
from sqlalchemy.orm import Mapped, mapped_column


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    ean: Mapped[str] = mapped_column(
        String(13),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    inserted_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    selling_place: Mapped[SellingPlaceEnum] = mapped_column(
        Enum(SellingPlaceEnum), nullable=False
    )
    picture: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
