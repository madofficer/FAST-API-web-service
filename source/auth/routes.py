from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from ..repository.main import get_session
from .utils import create_access_token, decode_token, PasswordCheck
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer

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


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    username = login_data.username
    password = login_data.password

    user = await user_service.get_user(username, session)

    if user and PasswordCheck.verify_password(password, user.password_hash):
        user_data = {"username": username, "user_uuid": str(user.uuid)}

        access_token = create_access_token(user_data=user_data)

        refresh_token = create_access_token(
            user_data=user_data, refresh=True, expiry=timedelta(days=2)
        )

        return JSONResponse(
            content={
                "message": "Logged in successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {"username": user.username, "uuid": str(user.uuid)},
            }
        )
        # todo: custom errors [auth error]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or Expired Token"
        )
