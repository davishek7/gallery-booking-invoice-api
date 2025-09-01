from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class ImageCategory(str, Enum):
    hero = "hero"
    gallery = "gallery"


class ImageUploadSchema(BaseModel):
    category: ImageCategory


class ImageResponse(BaseModel):
    id: str
    category: str
    url: str
    created_at: datetime
