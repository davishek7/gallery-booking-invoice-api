from fastapi import APIRouter, Depends, Form, UploadFile, File
from ..configs.dependency import get_gallery_service, get_cloudinary_service
from ..schemas.gallery_schema import ImageCategory

router = APIRouter()


@router.post("/")
async def upload_image(
    category: ImageCategory = Form(...),
    file: UploadFile = File(...),
    gallery_service=Depends(get_gallery_service),
    cloudinary_service=Depends(get_cloudinary_service),
):
    return await gallery_service.upload(category, file, cloudinary_service)


@router.get("/")
async def get_images(
    gallery_service=Depends(get_gallery_service),
    cloudinary_service=Depends(get_cloudinary_service),
):
    return await gallery_service.get_images(cloudinary_service)
