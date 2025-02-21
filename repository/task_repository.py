from uuid import uuid4
from domain.interfaces import TaskRepository
from domain.task import Task


class TaskRepositoryIml(TaskRepository):
    def __init__(self):
        self.tasks = {}

    def create_task(self, description: str) -> Task:
        task_id = str(uuid4())
        task = Task(id=task_id, description=description)
        self.tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Task:
        return self.tasks.get(task_id)

    def update_task(self, task: Task) -> None:
        self.tasks[task.id] = task
