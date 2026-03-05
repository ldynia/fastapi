from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from config.service import DEBUG
from config.service import POSTGRES_ASYNC_URL
from config.service import POSTGRES_SYNC_URL


async_engine = create_async_engine(POSTGRES_ASYNC_URL, echo=DEBUG, future=True)
sync_engine = create_engine(POSTGRES_SYNC_URL, echo=DEBUG, future=True)


async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


sync_session = sessionmaker(
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


def get_sync_session() -> Session:
    with sync_session() as session:
        yield session
