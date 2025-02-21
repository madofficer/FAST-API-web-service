from time import localtime, strftime, sleep
import threading


class Worker:
    def __init__(self, db, task_id):
        self.db = db
        self.task_id = task_id

    def run(self):
        self.db.update_task(
            self.task_id,
            status='running',
            log=f'Task started at {strftime("%H:%M:%S", localtime())}'
        )

        for i in range(1, 6):
            sleep(3)
            self.db.update_task(self.task_id, log=f'iter {i} done')

        self.db.update_task(
            self.task_id,
            status='completed',
            log=f'Task done successfully at {strftime("%H:%M:%S", localtime())}',
            result='ZOV'
        )

def start_task(db, task_id):
    worker = Worker(db, task_id)
    thread = threading.Thread(target=worker.run)
    thread.start()
