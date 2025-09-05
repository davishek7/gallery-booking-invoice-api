from fastapi import status
from pydantic import EmailStr
from bson import ObjectId  # type: ignore
from ..schemas.auth_schema import LoginSchema, RegisterSchma
from ..utils.auth import hash_password, verify_password, generate_auth_tokens
from ..exceptions.custom_exception import AppException
from ..utils.serializers import serialize_user
from ..utils.responses import success_response


class AuthService:
    def __init__(self, collection):
        self.collection = collection

    async def _authenticate(self, email: EmailStr, password: str):
        user = await self.collection.find_one({"email": email})
        if not user or not verify_password(password, user["password"]):
            raise AppException(
                "Invalid email or password.", status.HTTP_401_UNAUTHORIZED
            )
        sub = {"user_id": str(user["_id"]), "email": user["email"]}
        return {"user": serialize_user(user), "auth_tokens": generate_auth_tokens(sub)}

    async def login(self, login_schema: LoginSchema):
        login_creds = login_schema.model_dump()
        user_with_tokens = await self._authenticate(
            login_creds["email"], login_creds["password"]
        )
        return success_response(
            "Login successful", status.HTTP_200_OK, data=user_with_tokens
        )

    async def register(self, register_schema: RegisterSchma):
        user_data = register_schema.model_dump()
        user_data["password"] = hash_password(user_data["password"])
        await self.collection.insert_one(user_data)
        return success_response(
            "User account created successfully", status.HTTP_201_CREATED
        )

    async def refresh(self, sub):
        return success_response(
            "Tokens refreshed successfully",
            status.HTTP_200_OK,
            data=generate_auth_tokens(sub),
        )

    async def profile(self, user_id: str):
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return success_response(
            "Profile fetched successfully", status.HTTP_200_OK, serialize_user(user)
        )
