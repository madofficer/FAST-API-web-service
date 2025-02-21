from domain.interfaces import TaskRepository
from domain.task import Task


class CreateTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, description: str) -> Task:
        task = self.task_repository.create_task(description)
        return task
