from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from pymongo.errors import DuplicateKeyError  # type: ignore
from ..utils.responses import error_response
from .custom_exception import AppException


def register_exception_handlers(app):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return error_response(exc.message, exc.status_code, exc.errors)

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errors = [
            {
                "field": ".".join(str(loc) for loc in err["loc"][1:]),
                "message": err["msg"],
            }
            for err in exc.errors()
        ]
        return error_response(
            "Invalid data provided", status.HTTP_422_UNPROCESSABLE_ENTITY, errors
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return error_response(exc.detail, exc.status_code)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        print(f"Unhandled error: {exc}")  # Optional: log or notify
        return error_response(
            "Internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @app.exception_handler(DuplicateKeyError)
    async def handle_duplicate_key_error(request: Request, exc: DuplicateKeyError):
        return error_response(
            "Email or username already exists", status.HTTP_400_BAD_REQUEST
        )
