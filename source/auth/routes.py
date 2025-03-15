from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreateModel, UserModel
from .service import UserService
from ..repository.main import get_session

auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    "/register", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_Account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    username = user_data.username
    print(username)
    print(session)
    user_exists = await user_service.user_exists(username, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already Exists"
        )
    else:
        new_user = await user_service.create_user(user_data, session)
        return new_user
