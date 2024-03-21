from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.dependencies import DBSession
from src.models import User
from src.schemas import UserDetail, UserRegisterForm, TokenPairDetail, UserLoginForm, TokenRefreshForm
from src.utils import PasswordContext, jwt, oauth2

app = FastAPI()


@app.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDetail
)
async def register(session: DBSession, data: UserRegisterForm):
    user = User(
        **data.model_dump(exclude={"confirm_password"}) | {
            "password": PasswordContext.hash(password=data.password)
        }
    )
    session.add(instance=user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email exist")
    else:
        await session.refresh(instance=user)
    return UserDetail.model_validate(obj=user, from_attributes=True)


@app.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenPairDetail
)
async def login(session: DBSession, data: UserLoginForm):
    user = await session.scalar(
        select(User).filter(User.email == data.email)  # noqa
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")

    if not PasswordContext.verify(password=data.password, password_hash=user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect password")

    payload = {
        "sub": user.id
    }
    access_token = jwt.create_access_token(payload=payload)
    refresh_token = jwt.create_refresh_token(payload=payload)
    return TokenPairDetail(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=jwt.token_type,
        expire=jwt.access_exp
    )


@app.post(
    path="/refresh",
    response_model=TokenPairDetail,
    status_code=status.HTTP_200_OK
)
async def refresh(data: TokenRefreshForm):
    try:
        payload = jwt.verify_refresh_token(jwt=data.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")

    payload = {
        "sub": payload.get("sub")
    }
    access_token = jwt.create_access_token(payload=payload)
    refresh_token = jwt.create_refresh_token(payload=payload)
    return TokenPairDetail(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=jwt.token_type,
        expire=jwt.access_exp
    )


@app.get(
    path="/login/google",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
)
async def login_google(request: Request):
    return RedirectResponse(url=oauth2.auth_url(redirect_url=request.url_for("google_oauth")))


@app.get(
    path="/auth/google",
    name="google_oauth",
    response_model=TokenPairDetail,
    include_in_schema=False
)
async def auth_google(session: DBSession, code: str = Query(default=...)):
    try:
        user = oauth2.validate(code=code)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    else:
        user = await session.scalar(
            select(User).filter(User.email == user.get("email"))
        )
        if user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        payload = {
            "sub": user.id
        }
        access_token = jwt.create_access_token(payload=payload)
        refresh_token = jwt.create_refresh_token(payload=payload)
        return TokenPairDetail(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=jwt.token_type,
            expire=jwt.access_exp
        )

if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host="0.0.0.0",
        port=80
    )
