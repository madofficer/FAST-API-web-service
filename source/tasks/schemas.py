import uuid
from pydantic import BaseModel


class Task(BaseModel):
    uuid: uuid.UUID
    title: str
    code: str
    status: str
    result: str

    class Config:
        scheme_extra = {
            "example": {
                "id": 1,
                "title": "Task Master",
                "description": "Challenge",
                "status": "pending",
            }
        }


class TaskCreateModel(BaseModel):
    title: str
    code: str
