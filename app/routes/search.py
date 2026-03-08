from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from app.configs.dependency import get_search_service
from app.security.jwt import access_security


router = APIRouter()


@router.get("/")
async def search(
    q: str,
    search_service=Depends(get_search_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await search_service.search(q)
