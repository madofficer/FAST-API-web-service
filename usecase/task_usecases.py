from domain.task import Task
from domain.interfaces import TaskRepository
from usecase.worker import start_task


class TaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, task_id) -> Task:
        pass


class CreateTaskUseCase(TaskUseCase):
    def execute(self, description: str) -> Task:
        task = self.task_repository.create_task(description)
        start_task(self.task_repository, task.id)
        return task


class GetTaskStatusUseCase(TaskUseCase):
    def execute(self, task_id: str) -> Task:
        return self.task_repository.get_task(task_id)


class GetTaskResultUseCase(TaskUseCase):
    def execute(self, task_id: str) -> str:
        return self.task_repository.get_task(task_id).result
