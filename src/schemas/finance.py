from decimal import Decimal

from pydantic import Field, PositiveInt

from .base import Schema
from src.enum import ExpenseType

__all__ = [
    "FinanceCreateForm",
    "FinanceDetail",
    "FinanceEditForm",
]


class FinanceCreateForm(Schema):
    amount: Decimal = Field(
        default=...,
        title="Amount",
        examples=[100.50],
        gt=0,
        decimal_places=2
    )
    type: ExpenseType = Field(
        default=...,
        title="Expenses Type"
    )


class FinanceEditForm(FinanceCreateForm):
    ...


class FinanceDetail(FinanceCreateForm):
    id: PositiveInt = Field(
        default=...,
        title="Finance ID"
    )
