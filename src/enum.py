from enum import StrEnum

__all__ = [
    "ExpenseType",
]


class ExpenseType(StrEnum):
    Income: str = "income"
    Outcome: str = "outcome"
