import uuid
from src.context import request_id
from fastapi import Request, Response
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id.set(str(uuid.uuid4()))
        response = await call_next(request)
        return response
