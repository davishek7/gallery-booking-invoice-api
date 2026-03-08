from datetime import timedelta
from app.configs.settings import settings
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer  # type: ignore


access_security = JwtAccessBearer(
    settings.SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_TIMEDELTA)),
)

refresh_security = JwtRefreshBearer(
    settings.SECRET_KEY,
    auto_error=True,
    refresh_expires_delta=timedelta(days=int(settings.REFRESH_TOKEN_EXPIRE_TIMEDELTA)),
)


def generate_auth_tokens(sub: dict) -> dict:
    return {
        "access_token": access_security.create_access_token(sub),
        "refresh_token": refresh_security.create_refresh_token(sub),
    }
