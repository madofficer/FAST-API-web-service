from typing import List
from source.repository.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, status, HTTPException, Depends
from source.tasks.schemas import Task, TaskCreateModel
from source.tasks.service import TaskService
from source.auth.dependencies import AccessTokenBearer

task_router = APIRouter()
task_service = TaskService()
access_token_bearer = AccessTokenBearer()


# todo: admin endpoint
@task_router.get("/", response_model=List[Task])
async def get_all_tasks(
    session: AsyncSession = Depends(get_session),
    credentials: dict = Depends(access_token_bearer),
):
    tasks = await task_service.get_all_tasks(session)
    return tasks


@task_router.get("/user", response_model=List[Task])
async def get_all_user_tasks(
    session: AsyncSession = Depends(get_session),
    credentials: dict = Depends(access_token_bearer),
):
    user_uuid = credentials.get("user")["user_uuid"]
    tasks = await task_service.get_all_user_tasks(user_uuid, session)
    return tasks


@task_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Task)
async def create_task(
    task_data: TaskCreateModel,
    session: AsyncSession = Depends(get_session),
    credentials: dict = Depends(access_token_bearer),
) -> dict:
    user_uuid = credentials.get("user")["user_uuid"]
    new_task = await task_service.create_task(task_data, user_uuid, session)

    return new_task


@task_router.get("/{task_uuid}")
async def get_task(
    task_uuid: str,
    session: AsyncSession = Depends(get_session),
    credentials: dict = Depends(access_token_bearer),
):
    task = await task_service.get_task(task_uuid, session)

    if task:
        return task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not Found"
        )


@task_router.get("/{task_id}/status", status_code=status.HTTP_200_OK)
async def get_task_status(task_id, session: AsyncSession = Depends(get_session)):
    task = await get_task(task_id, session, Depends(access_token_bearer))
    return {"task_status": task.status}


@task_router.get("/{task_id}/result", status_code=status.HTTP_200_OK,)
async def get_task_result(
    task_id,
    session: AsyncSession = Depends(get_session),
):
    task = await get_task(task_id, session, Depends(access_token_bearer))
    return {"task_result": task.result}


@task_router.patch("/task_uuid", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def update_task(
    task_uuid: str,
    session: AsyncSession = Depends(get_session),
    credentials: dict = Depends(access_token_bearer),
):
    NotImplementedError()


@task_router.delete("/{task_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_uuid: str,
    session: AsyncSession = Depends(get_session),
    credentials: dict = Depends(access_token_bearer),
):
    task_to_del = await task_service.delete_task(task_uuid, session)
    if task_to_del:
        print("Task deleted")
        return {"Task deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not Found"
        )
