from .jwt import *
from .oauth import *
from .password import *
from src.settings import settings

jwt = JWT(
    access_secret_key=settings.JWT_ACCESS_SECRET_KEY.get_secret_value(),
    access_exp=settings.JWT_ACCESS_EXP,
    access_algorithm=settings.JWT_ACCESS_ALGORITHM,
    refresh_secret_key=settings.JWT_REFRESH_SECRET_KEY.get_secret_value(),
    refresh_exp=settings.JWT_REFRESH_EXP,
    refresh_algorithm=settings.JWT_REFRESH_ALGORITHM
)
oauth2 = OAuth2(
    client_id=settings.GOOGLE_CLIENT_ID.get_secret_value(),
    client_token=settings.GOOGLE_CLIENT_TOKEN.get_secret_value(),
    provider="google",
    scopes=settings.GOOGLE_SCOPES,
)


__all__ = [
    "jwt",
    "PasswordContext",
    "oauth2",
]
