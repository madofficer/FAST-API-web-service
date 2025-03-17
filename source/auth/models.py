from typing import List

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from source.tasks import models
from uuid import UUID, uuid4


class User(SQLModel, table=True):
    __tablename__ = "users"
    uuid: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    username: str
    password_hash: str = Field(exclude=True)
    tasks: List["models.Task"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"
