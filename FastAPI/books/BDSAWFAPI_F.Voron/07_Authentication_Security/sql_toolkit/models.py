import secrets
from datetime import datetime, timezone
from typing import Union

from sqlalchemy import select, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from utils import security_util


class Base(DeclarativeBase):
    # SQLAlchemy object contains database schema information
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True,
    )
    email: Mapped[str] = mapped_column(
        String(255), index=True, unique=True, nullable=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False,
    )


class AccessToken(Base):
    __tablename__ = "access_tokens"

    # string for authentication in requests
    access_token: Mapped[str] = mapped_column(
        String(255), primary_key=True, default=security_util.generate_token,
    )
    # foreign key to users table identifying user for token
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False,
    )
    # default validity of 24 hours
    expiration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, 
        default=security_util.get_expiration_date,
    )
    # relationship to access the user entity from an access token object
    # always retrieve the user when querying for an access token
    user: Mapped[User] = relationship("User", lazy="joined")

    def max_age(self) -> int:
        delta = self.expiration_date - datetime.now(tz=timezone.utc)
        return int(delta.total_seconds())