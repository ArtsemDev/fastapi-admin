from fastapi import APIRouter

from api.handlers import v1


router = APIRouter(prefix="/api")
router.include_router(router=v1.router)
