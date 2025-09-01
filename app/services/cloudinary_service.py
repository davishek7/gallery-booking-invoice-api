import cloudinary.uploader  # type: ignore
from cloudinary.utils import cloudinary_url  # type: ignore
from ..configs.settings import settings


class CloudinaryService:
    def __init__(self):
        pass

    async def upload(self, file):
        return cloudinary.uploader.upload(
            file.file,
            folder=settings.GALLERY_FOLDER_NAME,
            unique_filename=True,
        )

    async def format_secure_url(self, public_id):
        url, _ = cloudinary_url(public_id, secure=True)
        return url
