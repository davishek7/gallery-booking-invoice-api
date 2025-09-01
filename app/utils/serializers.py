from cloudinary.utils import cloudinary_url
from ..schemas.gallery_schema import ImageResponse


def serialize_image(image: dict) -> ImageResponse:
    image["id"] = str(image["_id"])
    image["url"] = cloudinary_url(image["public_id"])[0]
    del image["_id"]
    return ImageResponse(**image)
