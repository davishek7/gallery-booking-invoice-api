from fastapi import APIRouter, Depends, status, Security
from ..schemas.contact_schema import ContactIn
from ..configs.dependency import get_contact_service
from ..utils.auth import access_security
from fastapi_jwt import JwtAuthorizationCredentials  # type: ignore

router = APIRouter()


@router.post("/")
async def create(
    contact_schema: ContactIn, contact_service=Depends(get_contact_service)
):
    return await contact_service.create(contact_schema)


@router.get("/")
async def get_list(
    contact_service=Depends(get_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await contact_service.get_list()


@router.get("/{contact_id}")
async def get(
    contact_id: str,
    contact_service=Depends(get_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await contact_service.get(contact_id)


@router.patch("/{contact_id}")
async def update(
    contact_id: str,
    contact_service=Depends(get_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await contact_service.update(contact_id)


@router.delete("/{contact_id}")
async def delete(
    contact_id: str,
    contact_service=Depends(get_contact_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await contact_service.delete(contact_id)
