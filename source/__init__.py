from fastapi import FastAPI

from source.tasks.routes import task_router
from contextlib import asynccontextmanager
from source.repository.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is running")
    await init_db()
    yield
    print("Server shut down")

app = FastAPI(
    title="TaskRunner",
    description="A REST API for a task web service",
    lifespan=life_span
)

app.include_router(task_router, prefix="/tasks", tags=["tasks"])

