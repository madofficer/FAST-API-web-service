from uuid import UUID, uuid4
from typing import Optional

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from source.auth import models


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    uuid: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    title: str
    description: str
    status: str
    result: str = Field(default=None)
    user_uuid: Optional[UUID] = Field(default=None, foreign_key="users.uuid")
    user: Optional["models.User"] = Relationship(back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.title}>"

    class Config:
        scheme_extra = {
            "example": {
                "uuid": "some_uuid",
                "title": "Task Master",
                "description": "Challenge",
                "status": "pending",
            }
        }
