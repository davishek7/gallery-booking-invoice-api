from pydantic import BaseModel, Field
from datetime import datetime


class ContactIn(BaseModel):
    name: str
    phone_number: int
    message: str
    read_status: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)


class ContactResponse(BaseModel):
    id: str
    name: str
    phone_number: int
    message: str
    read_status: bool
    created_at: str


class ContactSearchResult(BaseModel):
    id: str
    name: str
