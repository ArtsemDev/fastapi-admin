from abc import ABC, abstractmethod

from httpx import Client, codes

__all__ = [
    "OAuth2",
]


class AbstractOAuth2(ABC):

    def __init__(
            self,
            client_id: str,
            client_token: str,
            scopes: list[str],
            provider: str
    ) -> None:
        if provider.lower() not in ("google", "yandex"):
            raise ValueError("incorrect provider")

        self.client_id = client_id
        self.client_token = client_token
        self.scopes = scopes
        self.provider = provider.lower()

    @abstractmethod
    def auth_url(self, redirect_url: str) -> str:
        pass

    @abstractmethod
    def validate(self, code: str) -> dict:
        pass


class OAuth2(AbstractOAuth2):

    def auth_url(self, redirect_url: str) -> str:
        if self.provider == "google":
            return (f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.client_id}"
                    f"&redirect_uri={redirect_url}&scope={'%20'.join(self.scopes)}&access_type=offline")

    def _google_validate(self, code: str) -> dict:
        token_url = "https://accounts.google.com/o/oauth2/token"
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_token,
            "redirect_uri": self.redirect_url,
            "grant_type": "authorization_code",
        }
        with Client() as client:
            response = client.post(url=token_url, data=data)
            if codes.is_success(value=response.status_code):
                access_token = response.json().get("access_token")
                user_info = client.get(
                    "https://www.googleapis.com/oauth2/v1/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                return user_info.json()
            raise ValueError("incorrect code")

    def validate(self, code: str) -> dict:
        if self.provider == "google":
            return self._google_validate(code=code)
