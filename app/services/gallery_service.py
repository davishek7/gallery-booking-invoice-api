from fastapi import status
from bson import ObjectId  # type: ignore
from datetime import datetime
from ..services.cloudinary_service import CloudinaryService
from ..utils.serializers import serialize_image
from ..utils.responses import success_response
from ..schemas.gallery_schema import ImageCategory
from ..exceptions.custom_exception import AppException


class GalleryService:
    def __init__(self, collection, cloudinary_service: CloudinaryService):
        self.collection = collection
        self.cloudinary_service = cloudinary_service
        self.MAX_SIZE = 10 * 1024 * 1024  # 10MB

    async def create(self, category, files):
        for file in files:
            content = await file.read()
            file_size = len(content)
            if file_size > self.MAX_SIZE:
                return AppException(
                    "File size too large (>10MB)", status.HTTP_400_BAD_REQUEST
                )

            result = await self.cloudinary_service.upload(content)

            photo_doc = {
                "category": category,
                "public_id": result["public_id"],
                "folder": result["folder"],
                "created_at": datetime.now(),
            }
            await self.collection.insert_one(photo_doc)
        return success_response("Images upload successfully", status.HTTP_201_CREATED)

    async def get_list(self, limit: int, offset: int, category: ImageCategory = None):
        query = {"category": category} if category is not None else {}
        cursor = self.collection.find(query).sort({"created_at": -1})
        if limit > 0:
            total = await self.collection.count_documents({"category": "gallery"})
            cursor = cursor.skip(offset).limit(limit)
        images = [serialize_image(doc) async for doc in cursor]
        if not images:
            return success_response(
                "No image found",
                status.HTTP_200_OK,
                data={"images": [], "limit": 0, "total": total},
            )
        return success_response(
            "Images fetched successfully",
            status.HTTP_200_OK,
            data={"images": images, "limit": limit, "total": total},
        )

    async def get(self, image_id: str):
        image = await self.collection.find_one({"_id": ObjectId(image_id)})
        if not image:
            raise AppException("Image not found", status.HTTP_404_NOT_FOUND)
        return success_response(
            "Image fetched successfully",
            status.HTTP_200_OK,
            data=serialize_image(image),
        )

    async def update(self, image_id: str, category):
        image = await self.collection.find_one({"_id": ObjectId(image_id)})
        if not image:
            raise AppException("Image not found", status.HTTP_404_NOT_FOUND)
        await self.collection.update_one(
            {"_id": ObjectId(image_id)}, {"$set": {"category": category}}
        )
        return success_response("Image updated successfully", status.HTTP_200_OK)

    async def delete(self, image_id):
        image = await self.collection.find_one({"_id": ObjectId(image_id)})
        if not image:
            raise AppException("Image not found", status.HTTP_404_NOT_FOUND)
        result = await self.cloudinary_service.destroy(image["public_id"])
        if result["result"] == "ok":
            await self.collection.delete_one({"_id": ObjectId(image_id)})
        return success_response("Image deleted successfully", status.HTTP_200_OK)
