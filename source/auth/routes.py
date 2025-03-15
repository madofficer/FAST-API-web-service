from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from ..repository.main import get_session
from .utils import create_access_token, decode_token, PasswordCheck
from fastapi.responses import JSONResponse

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


@auth_router.post(
    "/login"
)
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    username = login_data.username
    password = login_data.password

    user = await user_service.get_user(username, session)

    if user:
        user_data = {
            "username": username,
            "user_uuid": str(user.uuid)

        }
        # print(PasswordCheck.verify_password(password, user.password_hash))
        if PasswordCheck.verify_password(password, user.password_hash):
            access_token = create_access_token(
                user_data=user_data
            )

            refresh_token = create_access_token(
                user_data=user_data,
                refresh=True,
                expiry=timedelta(days=2)
            )

            return JSONResponse(
                content={
                    "message": "Logged in successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "username": user.username,
                        "uuid": str(user.uuid)
                    }
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
