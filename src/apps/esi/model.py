from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Boolean, Text
from sqlalchemy import Date, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from src.database.base import Base


class TimeStampedMixin:
    """Adds created_at and updated_at fields with timezone-aware UTC datetimes."""
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )


class SoftDeleteMixin:
    """Adds soft-delete fields."""
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class EsiUser(Base, TimeStampedMixin, SoftDeleteMixin):
    __tablename__ = "esi_users"

    id = Column(Integer, primary_key=True, index=True)

    esi_id = Column(String(255), unique=True, nullable=True)
    organization_tin = Column(String(255), nullable=True)
    organization_name = Column(String(255), nullable=True)
    position_name = Column(String(255), nullable=True)
    pin = Column(String(255), nullable=True)
    citizenship = Column(String(3), nullable=True)
    family_name = Column(String(255), nullable=True)
    given_name = Column(String(255), nullable=True)
    middle_name = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    gender = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)

    # Relationship to EsiToken
    esi_tokens = relationship("EsiToken", back_populates="esi_user")


class EsiToken(Base, TimeStampedMixin, SoftDeleteMixin):
    __tablename__ = "esi_tokens"

    id = Column(Integer, primary_key=True, index=True)

    esi_user_id = Column(Integer, ForeignKey("esi_users.id", ondelete="CASCADE"), nullable=False)
    esi_user = relationship("EsiUser", back_populates="esi_tokens")

    token_type = Column(String(255), nullable=False)
    token_value = Column(Text, nullable=False)
    expires_in = Column(DateTime(timezone=True), nullable=False)
    refresh_token = Column(String(255), nullable=False)
