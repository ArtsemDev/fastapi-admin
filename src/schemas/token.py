from .base import Schema

__all__ = [
    "TokenPairDetail",
    "TokenRefreshForm",
]


class TokenPairDetail(Schema):
    access_token: str
    refresh_token: str
    token_type: str
    expire: int


class TokenRefreshForm(Schema):
    refresh_token: str
