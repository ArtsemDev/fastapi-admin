from pydantic import PostgresDsn, SecretStr, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

__all__ = [
    "settings",
    "db_engine",
    "db_session_maker",
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env"
    )

    POSTGRES_URL: PostgresDsn
    JWT_ACCESS_SECRET_KEY: SecretStr
    JWT_REFRESH_SECRET_KEY: SecretStr
    JWT_ACCESS_ALGORITHM: str
    JWT_REFRESH_ALGORITHM: str
    JWT_ACCESS_EXP: PositiveInt
    JWT_REFRESH_EXP: PositiveInt
    GOOGLE_CLIENT_ID: SecretStr
    GOOGLE_CLIENT_TOKEN: SecretStr
    GOOGLE_SCOPES: list[str]


settings = Settings()
db_engine = create_async_engine(url=settings.POSTGRES_URL.unicode_string())
db_session_maker = async_sessionmaker(bind=db_engine)
