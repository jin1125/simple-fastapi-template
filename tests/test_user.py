"""ユーザー関連のテスト定義ファイル"""
import pytest
from httpx import AsyncClient
from starlette import status

from tests.constant import (
    TEST_UPDATE_USER_EMAIL,
    TEST_UPDATE_USER_NAME,
    TEST_UPDATE_USER_PASSWORD,
    TEST_USER_EMAIL,
    TEST_USER_NAME,
    TEST_USER_PASSWORD,
)


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient) -> None:
    """ユーザーの作成できるかテスト"""
    res = await async_client.post(
        "/user/create",
        json={
            "username": TEST_USER_NAME,
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
        },
    )
    assert res.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_read_user_me(
    async_client: AsyncClient,
    access_token: str,
) -> None:
    """ログインユーザーを取得できるかテスト"""
    res = await async_client.get(
        "/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_user(
    async_client: AsyncClient,
    access_token: str,
) -> None:
    """ログインユーザーを更新できるかテスト"""
    res = await async_client.patch(
        "/user/update",
        json={
            "username": TEST_UPDATE_USER_NAME,
            "email": TEST_UPDATE_USER_EMAIL,
            "password": TEST_UPDATE_USER_PASSWORD,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_user(
    async_client: AsyncClient,
    access_token: str,
) -> None:
    """ログインユーザーを削除できるかテスト"""
    res = await async_client.delete(
        "/user/delete",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == status.HTTP_204_NO_CONTENT
