from time import localtime, strftime, sleep
import threading

from domain.interfaces import TaskRepository


class TaskWorker:
    def __init__(self, task_repository: TaskRepository, task_id: str):
        self.task_repository = task_repository
        self.task_id = task_id

    def run(self):
        task = self.task_repository.get_task(self.task_id)
        if not task:
            return

        task.status = "running"
        task.log.append(f"Execution started at {strftime("%H:%M:%S", localtime())}")

        for i in range(1, 6):
            sleep(3)
            task.log.append(f"iter {i} running")
            self.task_repository.update_task(task)
        task.log.append(f'Executed at {strftime("%H:%M:%S", localtime())}')

        task.status = "Completed"
        task.result = "panda"
        self.task_repository.update_task(task)


def start_task(task_repository: TaskRepository, task_id: str):
    worker = TaskWorker(task_repository, task_id)
    thread = threading.Thread(target=worker.run)
    thread.start()
