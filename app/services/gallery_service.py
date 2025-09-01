from datetime import datetime, timezone
from ..configs.settings import settings
from ..services.cloudinary_service import CloudinaryService
from ..utils.serializers import serialize_image


class GalleryService:
    def __init__(self, collection):
        self.collection = collection

    async def upload(self, category, file, cloudinary_service: CloudinaryService):
        result = await cloudinary_service.upload(file)

        photo_doc = {
            "public_id": result["public_id"],
            "folder": result["folder"],
            "created_at": datetime.now(timezone.utc),
        }
        inserted = await self.collection.insert_one(photo_doc)

        return {
            "id": str(inserted.inserted_id),
            "category": category,
            "url": await cloudinary_service.format_secure_url(result["public_id"]),
        }

    async def get_images(self, cloudinary_service: CloudinaryService):
        cursor = self.collection.find().sort({"uploaded_at": -1})
        images = []
        async for doc in cursor:
            images.append(serialize_image(doc))
        return images
