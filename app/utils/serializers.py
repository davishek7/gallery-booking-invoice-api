from cloudinary.utils import cloudinary_url  # type: ignore
from ..schemas.gallery_schema import ImageResponse
from ..schemas.booking_schema import Booking
from ..schemas.auth_schema import UserResponse
from ..schemas.contact_schema import ContactResponse
from ..utils.datetime_formatter import format_datetime
from supabase import Client


def serialize_image(image: dict) -> ImageResponse:
    image["id"] = str(image["_id"])
    image["thumb_url"] = cloudinary_url(
        image["public_id"],
        height=72,
        crop="limit",  # keep aspect ratio, no stretching
        quality="auto",
    )[0]
    image["url"] = cloudinary_url(
        image["public_id"],
        height=500,
        crop="limit",  # keep aspect ratio, no stretching
        quality="auto",
    )[0]
    image["created_at"] = format_datetime(image["created_at"])
    del image["_id"]
    return ImageResponse(**image)


def serialize_booking(
    booking: dict, client: Client = None, bucket: str = None
) -> Booking:
    booking["id"] = str(booking["_id"])
    booking["created_at"] = format_datetime(booking["created_at"])
    booking["customer_name"] = booking["customer"]["name"]
    booking["customer_address"] = booking["customer"]["address"]
    booking["customer_phone_number"] = booking["customer"]["phone_number"]
    booking["items"] = [serialize_booking_item(item) for item in booking["items"]]
    booking["payments"] = [
        serialize_payment(payment) for payment in booking["payments"]
    ]
    if client and bucket:
        booking["invoice_url"] = (
            client.storage.from_(bucket).get_public_url(booking["invoice_file"])
            if "invoice_file" in booking
            else None
        )
        booking["download_url"] = (
            f"{client.storage.from_(bucket).get_public_url(booking['invoice_file'])}?download={booking['invoice_file']}"
            if "invoice_file" in booking
            else None
        )
    del booking["_id"]
    del booking["customer"]
    return Booking(**booking)


def serialize_payment(payment: dict) -> dict:
    payment["date"] = format_datetime(payment["date"])
    return payment


def serialize_booking_item(item: dict) -> dict:
    item["date"] = format_datetime(item["date"])
    return item


def serialize_user(user: dict) -> UserResponse:
    user["id"] = str(user["_id"])
    del user["_id"]
    user["created_at"] = format_datetime(user["created_at"])
    return UserResponse(**user)


def serialize_contact(contact: dict) -> ContactResponse:
    contact["id"] = str(contact["_id"])
    contact["created_at"] = format_datetime(contact["created_at"])
    del contact["_id"]
    return ContactResponse(**contact)
