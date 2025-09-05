from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterSchma(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    created_at: str
