import uuid as uuid_pkg
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg



class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    uuid: uuid_pkg.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid_pkg.uuid4
        )
    )
    title: str
    description: str
    status: str

    def __repr__(self):
        return f"<Task {self.title}>"

    class Config:
        scheme_extra = {
            "example": {
                    "uuid": "some_uuid",
                    "title": "Task Master",
                    "description": "Challenge",
                    "status": "pending"
            }
        }
