from re import compile
from typing import Annotated

from annotated_types import Predicate

__all__ = [
    "PasswordStr",
]

PASSWORD_PATTERN = compile(pattern=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,64}$")


def check_password(value: str) -> bool:
    return PASSWORD_PATTERN.fullmatch(string=value) is not None


PasswordStr = Annotated[str, Predicate(func=check_password)]
