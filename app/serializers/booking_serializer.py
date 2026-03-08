from app.schemas.booking_schema import BookingList, BookingResponse
from app.utils.datetime_formatter import format_display_datetime
from app.serializers.expense_serializer import serialize_expense
from app.utils.mongo import mongo_to_dict


def serialize_booking_list(booking: dict) -> BookingList:
    booking = mongo_to_dict(booking)

    items = sorted(booking["items"], key=lambda item: item["date"])
    payments = sorted(booking.get("payments", []), key=lambda p: p["date"])

    data = {
        "id": booking["id"],
        "booking_id": booking["booking_id"],
        "customer_name": booking["customer"]["name"],
        "discount": booking["discount"],
        "invoice_file": booking.get("invoice_file"),
        "created_at": format_display_datetime(booking["created_at"]),
        "items": [serialize_booking_item(item) for item in items],
        "payments": [serialize_payment(payment) for payment in payments],
    }

    return BookingList(**data)


def serialize_booking(booking: dict) -> BookingResponse:
    booking = mongo_to_dict(booking)

    items = sorted(booking["items"], key=lambda item: item["date"])
    payments = sorted(booking.get("payments", []), key=lambda p: p["date"])

    data = {
        "id": booking["id"],
        "booking_id": booking["booking_id"],
        "customer_name": booking["customer"]["name"],
        "customer_address": booking["customer"]["address"],
        "customer_phone_number": booking["customer"]["phone_number"],
        "advance": booking["advance"],
        "discount": booking["discount"],
        "invoice_file": booking.get("invoice_file"),
        "created_at": format_display_datetime(booking["created_at"]),
        "items": [serialize_booking_item(item) for item in items],
        "payments": [serialize_payment(payment) for payment in payments],
        "expenses": [
            serialize_expense(expense) for expense in booking.get("expenses", [])
        ],
        "total_expense": booking.get("total_expense", 0),
    }

    return BookingResponse(**data)


def serialize_payment(payment: dict) -> dict:
    payment = dict(payment)
    payment["date"] = format_display_datetime(payment["date"])
    return payment


def serialize_booking_item(item: dict) -> dict:
    item = dict(item)
    item["date"] = format_display_datetime(item["date"])
    return item
