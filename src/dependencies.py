from annotated_types import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings import db_session_maker

__all__ = [
    "DBSession",
]


async def _create_db_session():
    session = db_session_maker()
    try:
        yield session
    finally:
        await session.aclose()


DBSession = Annotated[AsyncSession, Depends(dependency=_create_db_session)]
