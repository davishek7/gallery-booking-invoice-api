from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials  # type: ignore
from ..configs.dependency import get_stat_service
from ..utils.auth import access_security


router = APIRouter()


@router.get("/")
async def stats(
    stat_service=Depends(get_stat_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await stat_service.stats()


@router.get("/income/")
async def get_yearly_income(
    stat_service=Depends(get_stat_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await stat_service.get_yearly_income()
