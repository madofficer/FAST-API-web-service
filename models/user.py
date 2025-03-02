from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship

from repository.database import Base

class User(Base):
    # __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # task = relationship("Task",
    #                     back_populates="users",
    #                     cascade="all, delete-orphan")

    class Config:
        scheme_extra = {
            "example": {
                "id": 1,
                "username": "centurion",
                "password": "qwerty123",
            }
        }

# class User(BaseModel):
#     username: str
#     password: str
#     tasks: Optional[List[Task]]
#
#     class Config:
#         from_attributes = True
#         scheme_extra = {
#             "example": {
#                 "username": "centurion",
#                 "tasks": [],
#             }
#         }


# class UserSignIN(User):
#     username: str
#     password: str
#
#     class Config:
#         scheme_extra = {
#             "example": {
#                 "username": "centurion",
#                 "tasks": []
#             }
#         }


# class UserBase(BaseModel):
#     username: str
#
# class UserCreate(UserBase):
#     password: str
#
# class User(UserBase):
#     id: int
#     tasks: List[Task] = []
#
#     class Config:
#         from_attributes = True
#         scheme_extra = {
#                     "example": {
#                         "username": "centurion",
#                         "tasks": [],
#                     }
#                 }
