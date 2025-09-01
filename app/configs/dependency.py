from ..configs.db import get_db
from ..services.gallery_service import GalleryService
from ..services.cloudinary_service import CloudinaryService
from ..services.booking_service import BookingService


async def get_gallery_service() -> GalleryService:
    db = get_db()
    return GalleryService(db["gallery"])


async def get_cloudinary_service() -> CloudinaryService:
    return CloudinaryService()


async def get_booking_service() -> BookingService:
    db = get_db()
    return BookingService(db["booking"])
