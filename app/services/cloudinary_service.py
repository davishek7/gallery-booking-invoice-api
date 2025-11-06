import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from ..configs.settings import settings


class CloudinaryService:
    def __init__(self):
        pass

    async def upload(self, file):
        return cloudinary.uploader.upload(
            file.file,
            folder=settings.GALLERY_FOLDER_NAME,
            width=1200,
            crop="limit",
            quality="auto:good",
            unique_filename=True,
        )

    async def destroy(self, public_id):
        return cloudinary.uploader.destroy(public_id, invalidate=True)
