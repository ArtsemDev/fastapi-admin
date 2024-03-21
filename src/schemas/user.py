from typing import Self, Optional

from pydantic import EmailStr, Field, model_validator, PositiveInt, HttpUrl

from .base import Schema
from .types import PasswordStr

__all__ = [
    "UserDetail",
    "UserRegisterForm",
    "UserLoginForm",
]


class UserRegisterForm(Schema):
    email: EmailStr = Field(
        default=...,
        title="User email",
        examples=["jone@doe.com"]
    )
    password: PasswordStr = Field(
        default=...,
        title="Password",
        examples=["VeryStrongPassword1!"]
    )
    confirm_password: PasswordStr = Field(
        default=...,
        title="Confirm Password",
        examples=["VeryStrongPassword1!"]
    )

    @model_validator(mode="after")
    def validator(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("the password and the confirm_password do not match")

        return self


class UserLoginForm(Schema):
    email: EmailStr = Field(
        default=...,
        title="User email",
        examples=["jone@doe.com"]
    )
    password: PasswordStr = Field(
        default=...,
        title="Password",
        examples=["VeryStrongPassword1!"]
    )


class UserDetail(Schema):
    id: PositiveInt = Field(
        default=...,
        title="User ID",
        examples=[42]
    )
    email: EmailStr = Field(
        default=...,
        title="User email",
        examples=["jone@doe.com"]
    )
    icon: Optional[HttpUrl] = Field(
        default=None,
        title="Url to profile icon"
    )
