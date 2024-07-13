"""DB関連の定義ファイル"""
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from api.config import settings

Base: Any = declarative_base()


async_engine: AsyncEngine = create_async_engine(
    settings.get_async_url(),
    echo=settings.db_echo,
)
async_session: sessionmaker = sessionmaker(  # type: ignore
    bind=async_engine,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator:
    """
    非同期データベースセッションを取得

    Yields:
    - 非同期データベースセッション
    """
    async with async_session() as session:
        yield session
        await session.commit()
