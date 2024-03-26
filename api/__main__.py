from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from api.handlers import router
from src.enum import ExpenseType

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
app.add_middleware(
    middleware_class=GZipMiddleware
)
app.add_middleware(
    middleware_class=ProxyHeadersMiddleware,
    trusted_hosts=("*", )
)
app.include_router(router=router)


@app.get(path="/api/v1/expense_types", response_model=list[ExpenseType])
async def expense_type_list():
    return list(ExpenseType)


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host="0.0.0.0",
        port=80
    )
