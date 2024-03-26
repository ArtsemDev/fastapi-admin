from fastapi import APIRouter, HTTPException, Path
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.models import Finance
from src.settings import db_session_maker
from src.schemas import FinanceCreateForm, FinanceEditForm, FinanceDetail

__all__ = [
    "FinanceAPI",
]


class FinanceAPI(object):
    model = Finance
    session = db_session_maker
    create_schema = FinanceCreateForm
    edit_schema = FinanceEditForm
    detail_schema = FinanceDetail

    def __init__(self):
        self.router = APIRouter()
        self.prefix = f"/{self.model.__name__.lower()}"
        self.router.add_api_route(
            path=self.prefix,
            methods=["POST"],
            endpoint=self.create,
            status_code=status.HTTP_201_CREATED,
            response_model=self.detail_schema,
            response_class=ORJSONResponse
        )
        self.router.add_api_route(
            path=self.prefix,
            methods=["GET"],
            endpoint=self.list,
            status_code=status.HTTP_200_OK,
            response_model=list[self.detail_schema],
            response_class=ORJSONResponse
        )
        self.router.add_api_route(
            path=self.prefix + "/{pk}",
            methods=["GET"],
            endpoint=self.detail,
            status_code=status.HTTP_200_OK,
            response_model=self.detail_schema,
            response_class=ORJSONResponse
        )

    async def create(self, request: Request, data: create_schema):
        async with self.session() as session:
            obj = self.model(**data.model_dump(), user_id=request.state.user.get("sub"))
            session.add(instance=obj)
            try:
                await session.commit()
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect data")
            else:
                await session.refresh(instance=obj)
                return self.detail_schema.model_validate(obj=obj, from_attributes=True)

    async def detail(self, request: Request, pk: int = Path(ge=1)):
        async with self.session() as session:
            obj = await session.get(
                entity=self.model,
                ident=pk
            )
            if obj is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            if obj.user_id != request.state.user.get("sub"):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

            return self.detail_schema.model_validate(obj=obj, from_attributes=True)

    async def list(self, request: Request):
        async with self.session() as session:
            objs = await session.scalars(
                select(self.model)
                .filter(self.model.user_id == request.state.user.get("sub"))
                .order_by(self.model.date_created.desc())
            )
            return [self.detail_schema.model_validate(obj=obj, from_attributes=True) for obj in objs.all()]
