from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4


class User(SQLModel, table=True):
    __tablename__ = "users"
    uuid: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    username: str
    password_hash: str = Field(exclude=True)

    def __repr__(self):
        return f"<User {self.username}>"
