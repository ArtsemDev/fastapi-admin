from annotated_types import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from src.settings import db_session_maker

__all__ = [
    "DBSession",
    "authenticate",
]

from src.utils import jwt


async def _create_db_session():
    session = db_session_maker()
    try:
        yield session
    finally:
        await session.aclose()


async def _authenticate(request: Request):
    authorization = request.headers.get("authorization")
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    token = authorization.removeprefix("Bearer ")
    try:
        payload = jwt.verify_access_token(jwt=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'{e}')
    request.state.user = payload

DBSession = Annotated[AsyncSession, Depends(dependency=_create_db_session)]
authenticate = Depends(dependency=_authenticate)
