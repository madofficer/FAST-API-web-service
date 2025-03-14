from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from source.config import Config

DATABASE_URL = (f"postgresql+asyncpg://"
                f"{Config.DB_USER}:"
                f"{Config.DB_PASS}@"
                f"{Config.DB_HOST}:"
                f"{Config.DB_PORT}/"
                f"{Config.DB_NAME}")

async_engine = AsyncEngine(
    create_engine(
        url=DATABASE_URL,
        echo=True
    )
)

async def init_db() -> None:
    async with async_engine.begin() as conn:
        from source.tasks.models import Task

        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session