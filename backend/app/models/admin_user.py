from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.db.base import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )
