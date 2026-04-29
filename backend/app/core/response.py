from typing import Any
from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse


class ApiError(Exception):
    def __init__(self, code: int, message: str, http_status: int = 400):
        self.code = code
        self.message = message
        self.http_status = http_status


def ok(data: Any = None, message: str = "ok") -> dict:
    return {
        "code": 0,
        "message": message,
        "data": data,
        "request_id": str(uuid4()),
    }


def error_response(code: int, message: str, http_status: int) -> JSONResponse:
    return JSONResponse(
        status_code=http_status,
        content={
            "code": code,
            "message": message,
            "data": None,
            "request_id": str(uuid4()),
        },
    )


async def api_error_handler(_: Request, exc: ApiError) -> JSONResponse:
    return error_response(exc.code, exc.message, exc.http_status)


async def validation_error_handler(_: Request, exc: Exception) -> JSONResponse:
    return error_response(40001, str(exc), 422)

