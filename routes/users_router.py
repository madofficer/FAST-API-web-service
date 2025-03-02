from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_schema import UserSchema
from repository.database import async_session_maker
from models.user import User
router_users = APIRouter()

async def get_db():
    async with async_session_maker() as session:
        yield session

@router_users.post("/users")
async def create_user(user: UserSchema, session: AsyncSession = Depends(get_db)):
    db_user = User(username=user.username, password=user.password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@router_users.get("/users/")
async def read_users(session: AsyncSession = Depends(get_db)):
    query = select(User)
    users = await session.execute(query)
    return users.scalars().all()

