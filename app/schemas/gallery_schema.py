from pydantic import BaseModel
from enum import Enum


class ImageCategory(str, Enum):
    hero = "hero"
    gallery = "gallery"


class ImageResponse(BaseModel):
    id: str
    category: str
    thumb_url: str
    url: str
    created_at: str
