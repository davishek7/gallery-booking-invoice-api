from fastapi import APIRouter, Depends, Form, UploadFile, File, Security, Query
from typing import List
from ..configs.dependency import get_gallery_service
from ..schemas.gallery_schema import ImageCategory
from fastapi_jwt import JwtAuthorizationCredentials  # type: ignore
from ..utils.auth import access_security


router = APIRouter()


@router.post("/")
async def upload_image(
    category: ImageCategory = Form(...),
    files: List[UploadFile] = File(...),
    gallery_service=Depends(get_gallery_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await gallery_service.create(category, files)


@router.get("/")
async def get_images(
    limit: int = Query(0, ge=0),
    category: ImageCategory = None,
    gallery_service=Depends(get_gallery_service),
):
    return await gallery_service.get_list(limit, category)


@router.get("/{image_id}")
async def get_image(
    image_id: str,
    gallery_service=Depends(get_gallery_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await gallery_service.get(image_id)


@router.patch("/{image_id}")
async def update_image(
    image_id: str,
    category: ImageCategory = Form(...),
    gallery_service=Depends(get_gallery_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await gallery_service.update(image_id, category)


@router.delete("/{image_id}")
async def delete_image(
    image_id: str,
    gallery_service=Depends(get_gallery_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await gallery_service.delete(image_id)
