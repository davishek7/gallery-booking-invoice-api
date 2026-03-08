from cloudinary.utils import cloudinary_url
from app.schemas.gallery_schema import ImageResponse
from app.utils.datetime_formatter import format_display_datetime
from app.utils.mongo import mongo_to_dict


def serialize_image(image: dict) -> ImageResponse:
    image = mongo_to_dict(image)
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
    return ImageResponse(**image)
