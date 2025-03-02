from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.orm import relationship

from repository.database import Base


class Task(Base):
    # __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    # user = relationship("User", back_populates="tasks")

    class Config:
        scheme_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "description": "sth about task panda",
                "completed": False
            }
        }
