from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True