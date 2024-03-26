from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, BIGINT, VARCHAR, CheckConstraint, CHAR, ForeignKey, DECIMAL, Enum, DATE
from sqlalchemy.orm import relationship

from src.enum import ExpenseType
from .base import Base

__all__ = [
    "User",
    "Finance",
    "Base",
]


class User(Base):
    __table_args__ = (
        CheckConstraint("length(email) >= 5"),
        CheckConstraint("email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z]{2,}$'"),
    )

    if TYPE_CHECKING:
        id: int
        email: str
        password: str
        icon: str
        finances: list["Finance"]
    else:
        id = Column(BIGINT, primary_key=True)
        email = Column(VARCHAR(length=128), nullable=False, unique=True)
        password = Column(CHAR(length=60), nullable=False)
        icon = Column(VARCHAR(length=64), nullable=True)
        finances = relationship(argument="Finance", back_populates="user")

    def __str__(self) -> str:
        return self.email


class Finance(Base):
    __table_args__ = (
        CheckConstraint("amount > 0"),
    )

    if TYPE_CHECKING:
        id: int
        user_id: int
        amount: float
        type: ExpenseType
        date_created: date
        user: User
    else:
        id = Column(BIGINT, primary_key=True)
        user_id = Column(
            BIGINT,
            ForeignKey(
                column=User.id,
                ondelete="CASCADE",
                onupdate="CASCADE"
            ),
            nullable=False,
            index=True
        )
        amount = Column(DECIMAL(scale=2), nullable=False)
        type = Column(Enum(ExpenseType), nullable=False, index=True)
        date_created = Column(DATE, nullable=False, default=lambda: datetime.now().date())
        user = relationship(argument=User, back_populates="finances")
