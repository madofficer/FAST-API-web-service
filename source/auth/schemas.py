from typing import List

from pydantic import BaseModel, Field
from uuid import UUID, uuid4

from source.tasks.schemas import Task


class UserCreateModel(BaseModel):
    username: str = Field(max_length=10)
    password: str = Field(min_length=5)


class UserModel(BaseModel):
    uuid: UUID
    username: str
    password_hash: str = Field(exclude=True)


class UserTaskModel(UserModel):
    tasks: List[Task]


class UserLoginModel(BaseModel):
    username: str = Field(max_length=10)
    password: str = Field(min_length=5)
