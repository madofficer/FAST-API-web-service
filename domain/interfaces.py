from abc import ABC, abstractmethod
from domain.task import Task


class TaskRepository(ABC):
    """
    Interface for Task Repository
    """

    @abstractmethod
    def create_task(self, description: str) -> Task:
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def update_task(self, task: Task) -> None:
        pass

    @abstractmethod
    def delete_task(self, task: Task) -> None:
        pass
