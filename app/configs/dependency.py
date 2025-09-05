from ..configs.db import get_db
from ..services.gallery_service import GalleryService
from ..services.cloudinary_service import CloudinaryService
from ..services.booking_service import BookingService
from ..services.auth_service import AuthService
from ..services.contact_service import ContactService
from ..services.admin_stat_service import AdminStatService


async def get_cloudinary_service() -> CloudinaryService:
    return CloudinaryService()


async def get_gallery_service() -> GalleryService:
    db = get_db()
    cloudinary_service = CloudinaryService()
    return GalleryService(db["gallery"], cloudinary_service)


async def get_booking_service() -> BookingService:
    db = get_db()
    return BookingService(db["booking"])


async def get_auth_service() -> AuthService:
    db = get_db()
    return AuthService(db["user"])


async def get_contact_service() -> ContactService:
    db = get_db()
    return ContactService(db["contact"])


async def get_admin_stat_service() -> AdminStatService:
    db = get_db()
    return AdminStatService(db["gallery"], db["booking"], db["contact"])
