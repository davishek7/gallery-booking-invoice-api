from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials  # type: ignore
from ..schemas.auth_schema import LoginSchema, RegisterSchma
from ..configs.dependency import get_auth_service
from ..utils.auth import access_security, refresh_security


router = APIRouter()


@router.post("/login")
async def login(
    login_schema: LoginSchema,
    auth_service=Depends(get_auth_service),
):
    return await auth_service.login(login_schema)


@router.post("/register")
async def register(
    register_schema: RegisterSchma,
    auth_service=Depends(get_auth_service),
):
    return await auth_service.register(register_schema)


@router.post("/refresh")
async def refresh(
    auth_service=Depends(get_auth_service),
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    sub = credentials.subject
    return await auth_service.refresh(sub)


@router.get("/profile")
async def profile(
    auth_service=Depends(get_auth_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials["user_id"]
    return await auth_service.profile(user_id)
