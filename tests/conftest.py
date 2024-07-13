"""共通フィクスチャの定義ファイル"""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from api.config import settings
from api.database.db import Base, get_db
from api.main import app
from tests.constant import (
    ASYNC_TEST_DB_URL,
    TEST_TODO_DETAIL,
    TEST_TODO_DUE_DATE,
    TEST_TODO_TITLE,
    TEST_USER_EMAIL,
    TEST_USER_NAME,
    TEST_USER_PASSWORD,
)

async_test_engine: AsyncEngine = create_async_engine(
    ASYNC_TEST_DB_URL,
    echo=settings.test_db_echo,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    イベントループをオーバーライドするフィクスチャ

    Yields:
    - イベントループ
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_database() -> AsyncGenerator:
    """
    テスト用のテーブルをセットアップするフィクスチャ

    - 自動で実行されるフィクスチャ

    - テーブルを削除
    - テーブルを作成
    - テストを実行
    - テーブルを削除
    """
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator:
    """
    テスト用の非同期HTTPクライアントを提供するフィクスチャ

    - テスト用の非同期データベースセッションでオーバーライド
    - テスト用の非同期HTTPクライアントを提供

    Yields:
    - 非同期HTTPクライアント
    """
    app.dependency_overrides[get_db] = _get_test_db  # type:ignore

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


async def _get_test_db() -> AsyncGenerator:
    """
    テスト用の非同期データベースセッションを取得

    Yields:
    - 非同期データベースセッション
    """
    async_test_session: sessionmaker = sessionmaker(  # type: ignore
        bind=async_test_engine,
        class_=AsyncSession,
    )

    async with async_test_session() as session:
        yield session
        await session.commit()


@pytest_asyncio.fixture
async def access_token(async_client: AsyncClient) -> str:
    """
    テスト用ユーザーのアクセストークンを提供するフィクスチャ

    Args:
    - async_client: 非同期HTTPクライアント

    Returns:
    - アクセストークン
    """
    await async_client.post(
        "/user/create",
        json={
            "username": TEST_USER_NAME,
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
        },
    )
    res = await async_client.post(
        "/token",
        data={
            "username": TEST_USER_NAME,
            "password": TEST_USER_PASSWORD,
        },
    )
    data = res.json()
    return data["access_token"]


@pytest_asyncio.fixture
async def factory_todo(async_client: AsyncClient, access_token: str) -> None:
    """
    テスト用のTodoデータを作成するフィクスチャ

    Args:
    - async_client: 非同期HTTPクライアント
    - access_token:
    """
    await async_client.post(
        "/todo/create",
        json={
            "title": TEST_TODO_TITLE,
            "detail": TEST_TODO_DETAIL,
            "due_date": TEST_TODO_DUE_DATE,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
