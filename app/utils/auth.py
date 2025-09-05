from datetime import timedelta
from passlib.context import CryptContext  # type: ignore
from ..configs.settings import settings
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer  # type: ignore


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def generate_auth_tokens(sub: dict) -> dict:
    return {
        "access_token": access_security.create_access_token(sub),
        "refresh_token": refresh_security.create_refresh_token(sub),
    }
