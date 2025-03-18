from sqlmodel import select
from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreateModel
from .utils import PasswordCheck


class UserService:
    # @staticmethod
    async def get_user(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)

        result = await session.exec(statement)

        return result.first()

    async def user_exists(self, username, session: AsyncSession):
        user = await self.get_user(username, session)

        return True if user else False

    # @staticmethod
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password_hash = PasswordCheck.generate_password_hash(
            user_data_dict["password"]
        )

        session.add(new_user)
        await session.commit()

        return new_user
