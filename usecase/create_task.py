from domain.interfaces import TaskRepository
from domain.task import Task
from usecase.worker import start_task


class CreateTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, description: str) -> Task:
        task = self.task_repository.create_task(description)
        start_task(self.task_repository, task.id)
        return task
