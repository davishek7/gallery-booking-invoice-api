from app.schemas.contact_schema import ContactResponse
from app.utils.datetime_formatter import format_display_datetime
from app.utils.mongo import mongo_to_dict


def serialize_contact(contact: dict) -> ContactResponse:
    contact = mongo_to_dict(contact)

    contact["id"] = str(contact["_id"])
    contact["created_at"] = format_display_datetime(contact["created_at"])

    return ContactResponse(**contact)
