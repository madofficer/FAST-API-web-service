from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4


"""
class User:
    uuid: uuid.UUID
    username: str
    name: str
    password: str
"""

class User(SQLModel, table=True):
    __tablename__ = "users"
    uuid: UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid4
        )
    )
    username: str
    name: str
    password: str

    def __repr__(self):
        return f"<User {self.username}>"

