from app.schemas.auth_schema import UserResponse
from app.utils.datetime_formatter import format_display_datetime
from app.utils.mongo import mongo_to_dict


def serialize_user(user: dict) -> UserResponse:
    user = mongo_to_dict(user)

    user["created_at"] = format_display_datetime(user["created_at"])
    return UserResponse(**user)
