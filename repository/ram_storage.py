import json
import os
from uuid import uuid4


class RamStorage:
    def __init__(self):
        self.storage_dir = ""
        self.data = {}
        self.data_file = os.path.join(self.storage_dir, 'data.json')
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

        if not os.path.exists(self.data_file):
            print(self.data_file)
            with open(self.data_file, 'w') as df:
                json.dump({}, df)
        else:
            with open(self.data_file, 'r') as df:
                self.data = json.load(df)

    def _save_data(self):
        with open(self.data_file, 'w') as df:
            json.dump(self.data, df, indent=4)

    def create_task(self, task_data):
        task_id = str(uuid4())
        self.data[task_id] = {
            "name": "",
            "status": "pending",
            "data": task_data,
            "log": [],
            "result": None
        }

        self._save_data()
        return task_id

    def get_task(self, task_id):
        return self.data.get(task_id)

    def update_task(self, task_id, status=None, log=None, result=None):
        if task_id in self.data:
            if status:
                self.data[task_id]["status"] = status
            if log:
                self.data[task_id]["log"].append(log)
            if result:
                self.data[task_id]["result"] = result
        self._save_data()
