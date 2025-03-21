from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from source.tasks.models import Task
from source.tasks.schemas import TaskCreateModel
from uuid import UUID


class TaskService:
    async def get_all_tasks(self, session: AsyncSession):
        statement = select(Task).order_by(desc(Task.title))

        result = await session.exec(statement)

        return result.all()

    async def get_all_user_tasks(self, user_uuid: str, session: AsyncSession):
        statement = (
            select(Task).where(Task.user_uuid == user_uuid).order_by(desc(Task.title))
        )

        result = await session.exec(statement)

        return result.all()

    async def get_task(self, task_uuid: str, session: AsyncSession):
        if self.validate_uuid(task_uuid):
            statement = select(Task).where(Task.uuid == task_uuid)

            result = await session.exec(statement)

            return result.first() if result else None

    async def create_task(
        self, task_data: TaskCreateModel, user_uuid: str, session: AsyncSession
    ) -> dict:
        task_data_dict = task_data.model_dump()
        new_task = Task(**task_data_dict)
        new_task.user_uuid = user_uuid

        session.add(new_task)
        await session.commit()

        return new_task

    async def update_task(
        self, task_uuid: str, upd_data: TaskCreateModel, session: AsyncSession
    ):
        task_to_upd = self.get_task(task_uuid, session)
        if task_to_upd:
            upd_data_dict = upd_data.model_dump()
            for key, val in upd_data_dict.items():
                setattr(task_to_upd, key, val)
            await session.commit()
            return task_to_upd
        else:
            print("Task not Found")
            return None

    async def delete_task(self, task_uuid: str, session: AsyncSession):

        task_to_del = await self.get_task(task_uuid, session)
        if task_to_del:
            await session.delete(task_to_del)

            await session.commit()
            return True
        else:
            print("Task not Found")
            return None

    @staticmethod
    def validate_uuid(uuid_to_test, version=4):
        try:
            UUID(uuid_to_test, version=version)
        except ValueError:
            return False
        return True
