from uuid import uuid4

from domain.interfaces import TaskRepository


def gen_uuid(task_repository: TaskRepository) -> str:
    while True:
        task_id = str(uuid4())
        if task_id not in task_repository:
            return task_id
