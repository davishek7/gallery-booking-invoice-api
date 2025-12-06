from ..configs.db import get_db
from ..services.gallery_service import GalleryService
from ..services.cloudinary_service import CloudinaryService
from ..services.booking_service import BookingService
from ..services.auth_service import AuthService
from ..services.contact_service import ContactService
from ..services.admin_stat_service import AdminStatService
from ..services.supabase_service import SupabaseService
from ..services.r2_service import R2Service
from ..services.expense_service import ExpenseService


async def get_cloudinary_service() -> CloudinaryService:
    return CloudinaryService()


async def get_r2_service() -> R2Service:
    db = get_db()
    return R2Service(db["booking"])


async def get_supabase_service() -> SupabaseService:
    db = get_db()
    return SupabaseService(db["booking"])


async def get_gallery_service() -> GalleryService:
    db = get_db()
    cloudinary_service = CloudinaryService()
    return GalleryService(db["gallery"], cloudinary_service)


async def get_booking_service() -> BookingService:
    db = get_db()
    invoice_service = await get_r2_service()
    return BookingService(db["booking"], db["expense"], invoice_service)


async def get_auth_service() -> AuthService:
    db = get_db()
    return AuthService(db["user"])


async def get_contact_service() -> ContactService:
    db = get_db()
    return ContactService(db["contact"])


async def get_expense_service() -> ExpenseService:
    db = get_db()
    return ExpenseService(db["expense"], db["booking"])


async def get_admin_stat_service() -> AdminStatService:
    db = get_db()
    return AdminStatService(db["gallery"], db["booking"], db["contact"], db["expense"])
