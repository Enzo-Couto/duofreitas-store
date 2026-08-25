from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    image_url = Column(
        String(500),
        nullable=False
    )

    is_primary = Column(
        Boolean,
        default=False
    )

    sort_order = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    product = relationship(
        "Product",
        back_populates="images"
    )
