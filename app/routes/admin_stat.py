from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials  # type: ignore
from ..configs.dependency import get_admin_stat_service
from ..utils.auth import access_security


router = APIRouter()


@router.get("/stats")
async def stats(
    admin_stat_service=Depends(get_admin_stat_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await admin_stat_service.stats()
