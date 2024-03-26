from fastapi import APIRouter

from src.dependencies import authenticate
from .finance import FinanceAPI


router = APIRouter(prefix="/v1")
router.include_router(router=FinanceAPI().router, dependencies=[authenticate])
