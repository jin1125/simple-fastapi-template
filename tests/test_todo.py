"""Todo関連のテスト定義ファイル"""
import pytest
from httpx import AsyncClient
from starlette import status

from tests.constant import (
    TEST_TODO_DETAIL,
    TEST_TODO_DUE_DATE,
    TEST_TODO_TITLE,
    TEST_UPDATE_DONE,
    TEST_UPDATE_TODO_DETAIL,
    TEST_UPDATE_TODO_DUE_DATE,
    TEST_UPDATE_TODO_TITLE,
)


@pytest.mark.asyncio
async def test_create_todo(
    async_client: AsyncClient,
    access_token: str,
) -> None:
    """Todoを作成できるかテスト"""
    res = await async_client.post(
        "/todo/create",
        json={
            "title": TEST_TODO_TITLE,
            "detail": TEST_TODO_DETAIL,
            "due_date": TEST_TODO_DUE_DATE,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_read_todo_list(
    async_client: AsyncClient,
    access_token: str,
) -> None:
    """Todo一覧を取得できるかテスト"""
    res = await async_client.get(
        "/todo/list",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_read_todo_detail(
    async_client: AsyncClient,
    access_token: str,
    factory_todo: None,
) -> None:
    """Todo詳細を取得できるかテスト"""
    res = await async_client.get(
        "/todo/detail/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_todo(
    async_client: AsyncClient,
    access_token: str,
    factory_todo: None,
) -> None:
    """Todoを更新できるかテスト"""
    res = await async_client.patch(
        "/todo/update/1",
        json={
            "title": TEST_UPDATE_TODO_TITLE,
            "detail": TEST_UPDATE_TODO_DETAIL,
            "due_date": TEST_UPDATE_TODO_DUE_DATE,
            "done": TEST_UPDATE_DONE,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_todo(
    async_client: AsyncClient,
    access_token: str,
    factory_todo: None,
) -> None:
    """Todoを削除できるかテスト"""
    res = await async_client.delete(
        "/todo/delete/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == status.HTTP_204_NO_CONTENT
