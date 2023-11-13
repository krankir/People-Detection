import asyncio

from fastapi import FastAPI

from src.amqp.service_request import ServiceHandler
from src.middleware.middleware import RequestIdMiddleware
from src.tasks.router import router as tasks_router


app = FastAPI(
    debug=True,
)

app.add_middleware(RequestIdMiddleware)

app.include_router(tasks_router)


@app.on_event("startup")
async def start_listener():
    """Создаёт при старте приложения такску которая создаёт метод листен."""
    asyncio.create_task(ServiceHandler.listen())
