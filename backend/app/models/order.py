from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    func
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(30), nullable=False)

    subtotal = Column(
        Numeric(10, 2),
        nullable=False
    )

    shipping_cost = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False,
        default="pending"
    )

    payment_status = Column(
        String(50),
        nullable=False,
        default="pending"
    )

    mercadopago_payment_id = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
