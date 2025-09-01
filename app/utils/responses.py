from typing import Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message: str, status_code: int = 200, data: Any = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message,
            "data": jsonable_encoder(data),
        },
    )


def error_response(message: str, status_code: int = 400, errors: Any | None = None):
    return JSONResponse(
        status_code=status_code,
        content={"status": status_code, "message": message, "errors": errors},
    )
