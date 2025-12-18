from cloudinary.utils import cloudinary_url
from ..schemas.gallery_schema import ImageResponse, ImageSearchResult
from ..schemas.booking_schema import BookingList, BookingResponse, BookingSearchResult
from ..schemas.auth_schema import UserResponse
from ..schemas.contact_schema import ContactResponse, ContactSearchResult
from ..schemas.expense_schema import ExpenseResponse, ExpenseSearchResult
from ..utils.datetime_formatter import format_display_datetime, format_datetime


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
    image["created_at"] = format_display_datetime(image["created_at"])
    del image["_id"]
    return ImageResponse(**image)


def serialize_booking_list(
    booking: dict, total_expense: int = 0, get_presigned_url=None
) -> BookingList:
    booking["id"] = str(booking["_id"])
    booking["created_at"] = format_display_datetime(booking["created_at"])
    booking["customer_name"] = booking["customer"]["name"]
    booking["customer_address"] = booking["customer"]["address"]
    booking["customer_phone_number"] = booking["customer"]["phone_number"]
    booking["items"].sort(key=lambda item: item["date"])
    booking["items"] = [serialize_booking_item(item) for item in booking["items"]]
    booking["payments"].sort(key=lambda payment: payment["date"])
    booking["payments"] = [
        serialize_payment(payment) for payment in booking["payments"]
    ]
    booking["total_expense"] = total_expense

    # if get_presigned_url:
    #     booking["invoice_url"] = (
    #         get_presigned_url(booking["invoice_file"])
    #         if "invoice_file" in booking
    #         else None
    #     )

    del booking["_id"]
    del booking["customer"]
    return BookingList(**booking)


def serialize_booking(
    booking: dict, total_expense: int = 0, get_presigned_url=None
) -> BookingList:
    booking["id"] = str(booking["_id"])
    booking["created_at"] = format_display_datetime(booking["created_at"])
    booking["customer_name"] = booking["customer"]["name"]  # if get_presigned_url:
    #     booking["invoice_url"] = (
    #         get_presigned_url(booking["invoice_file"])
    #         if "invoice_file" in booking
    #         else None
    #     )
    booking["customer_address"] = booking["customer"]["address"]
    booking["customer_phone_number"] = booking["customer"]["phone_number"]
    booking["items"].sort(key=lambda item: item["date"])
    booking["items"] = [serialize_booking_item(item) for item in booking["items"]]
    booking["payments"].sort(key=lambda payment: payment["date"])
    booking["payments"] = [
        serialize_payment(payment) for payment in booking["payments"]
    ]
    booking["total_expense"] = total_expense

    # if get_presigned_url:
    #     booking["invoice_url"] = (
    #         get_presigned_url(booking["invoice_file"])
    #         if "invoice_file" in booking
    #         else None
    #     )

    del booking["_id"]
    del booking["customer"]
    return BookingResponse(**booking)


def serialize_payment(payment: dict) -> dict:
    payment["date"] = format_display_datetime(payment["date"])
    return payment


def serialize_booking_item(item: dict) -> dict:
    item["date"] = format_display_datetime(item["date"])
    return item


def serialize_user(user: dict) -> UserResponse:
    user["id"] = str(user["_id"])
    del user["_id"]
    user["created_at"] = format_display_datetime(user["created_at"])
    return UserResponse(**user)


def serialize_contact(contact: dict) -> ContactResponse:
    contact["id"] = str(contact["_id"])
    contact["created_at"] = format_display_datetime(contact["created_at"])
    del contact["_id"]
    return ContactResponse(**contact)


def serialize_expense(expense: dict) -> ExpenseResponse:
    expense["id"] = str(expense["_id"])
    expense["display_date"] = format_display_datetime(expense["date"])
    expense["date"] = format_datetime(expense["date"])
    expense["created_at"] = format_display_datetime(expense["created_at"])
    del expense["_id"]
    return ExpenseResponse(**expense)


def serialize_search_results(
    data: dict, search_result_type: str
) -> (
    ImageSearchResult | BookingSearchResult | ContactSearchResult | ExpenseSearchResult
):
    if data["_id"]:
        data["id"] = str(data["_id"])

    del data["_id"]

    if search_result_type == "gallery":
        return ImageSearchResult(**data)

    if search_result_type == "booking":
        data["customer_name"] = data["customer"]["name"]
        return BookingSearchResult(**data)

    if search_result_type == "contact":
        return ContactSearchResult(**data)

    if search_result_type == "expense":
        return ExpenseSearchResult(**data)
