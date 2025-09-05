from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ImageCategory(str, Enum):
    hero = "hero"
    gallery = "gallery"


class ImageUploadSchema(BaseModel):
    category: ImageCategory
    created_at: datetime = Field(default_factory=datetime.now)


class ImageResponse(BaseModel):
    id: str
    category: str
    thumb_url: str
    url: str
    created_at: str
