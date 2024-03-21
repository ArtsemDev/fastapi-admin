from datetime import datetime, timedelta

from jwt import encode, decode
from jwt.exceptions import PyJWTError, InvalidTokenError, ExpiredSignatureError

__all__ = [
    "JWT",
]


class JWT(object):
    __slots__ = (
        "access_secret_key",
        "refresh_secret_key",
        "access_exp",
        "refresh_exp",
        "access_algorithm",
        "refresh_algorithm",
        "token_type"
    )

    def __init__(
            self,
            access_secret_key: str,
            refresh_secret_key: str,
            access_exp: int,
            refresh_exp: int,
            access_algorithm: str,
            refresh_algorithm: str
    ) -> None:
        self.access_secret_key = access_secret_key
        self.refresh_secret_key = refresh_secret_key
        self.access_exp = access_exp
        self.refresh_exp = refresh_exp
        self.access_algorithm = access_algorithm
        self.refresh_algorithm = refresh_algorithm
        self.token_type = "Bearer"

    @staticmethod
    def _create_jwt(*, payload: dict, exp: int, key: str, algorithm: str) -> str:
        if "sub" not in payload:
            raise AttributeError

        payload.update({"exp": datetime.now() + timedelta(minutes=exp)})
        return encode(payload=payload, key=key, algorithm=algorithm)

    @staticmethod
    def _verify_jwt(*, jwt: str, key: str, algorithm: str) -> dict:
        try:
            return decode(
                jwt=jwt,
                key=key,
                algorithms=[algorithm]
            )
        except ExpiredSignatureError:
            raise ValueError("Token has expired")
        except InvalidTokenError:
            raise ValueError("Invalid token or token type")
        except PyJWTError:
            raise ValueError("Incorrect token")

    def create_access_token(self, payload: dict) -> str:
        return self._create_jwt(
            payload=payload,
            exp=self.access_exp,
            algorithm=self.access_algorithm,
            key=self.access_secret_key
        )

    def create_refresh_token(self, payload: dict) -> str:
        return self._create_jwt(
            payload=payload,
            exp=self.refresh_exp,
            algorithm=self.refresh_algorithm,
            key=self.refresh_secret_key
        )

    def verify_access_token(self, jwt: str) -> dict:
        return self._verify_jwt(
            jwt=jwt,
            algorithm=self.access_algorithm,
            key=self.access_secret_key
        )

    def verify_refresh_token(self, jwt: str) -> dict:
        return self._verify_jwt(
            jwt=jwt,
            algorithm=self.refresh_algorithm,
            key=self.refresh_secret_key
        )
