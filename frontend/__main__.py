from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.settings import templating, static

app = FastAPI()
app.mount(path="/static", app=static, name="static")


@app.get(path="/")
async def index(request: Request):
    return templating.TemplateResponse(request=request, name="index.html")


@app.get(path="/login")
async def index(request: Request):
    return templating.TemplateResponse(request=request, name="sign-in.html")


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host="0.0.0.0",
        port=80
    )
