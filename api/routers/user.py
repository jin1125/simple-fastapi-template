"""ユーザー関連のパスオペレーション関数の定義ファイル"""
import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.db import get_db
from api.models import user as user_models
from api.schemas import user as user_schemas
from api.services import user as user_services

logger: logging.Logger = logging.getLogger(__name__)

router: APIRouter = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post(
    "/create",
    response_model=user_schemas.User,
    status_code=201,
    summary="ユーザーを作成",
)
async def create_user(
    create_user_data: user_schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    ユーザーを作成

    Args:
        create_user_data: ユーザーを作成するための情報
        db: 非同期のDBセッション

    Returns:
        作成したユーザー
    """
    return await user_services.create_user(create_user_data, db)


@router.get(
    "/me",
    response_model=user_schemas.User,
    summary="ログインユーザーを取得",
)
async def read_user_me(
    user_me: Annotated[user_models.User, Depends(user_services.get_user_me)],
):
    """
    ログインユーザーを取得

    Args:
        user_me: ログインユーザー

    Returns:
        ログインユーザー
    """
    if user_me:
        logger.info("ログインユーザーの取得に成功しました")
    return user_me


@router.patch(
    "/update",
    response_model=user_schemas.User,
    summary="ログインユーザーを更新",
)
async def update_user(
    user_me: Annotated[user_models.User, Depends(user_services.get_user_me)],
    update_user_data: user_schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    ログインユーザーを更新

    Args:
        user_me: ログインユーザー
        update_user_data: ログインユーザーを更新するための情報
        db: 非同期のDBセッション

    Returns:
        ログインユーザー
    """
    return await user_services.update_user(
        user_me,
        update_user_data,
        db,
    )


@router.delete(
    "/delete",
    response_model=None,
    status_code=204,
    summary="ログインユーザーを削除",
)
async def delete_user(
    user_me: Annotated[user_models.User, Depends(user_services.get_user_me)],
    db: AsyncSession = Depends(get_db),
):
    """
    ログインユーザーを削除

    Args:
        user_me: ログインユーザー
        db: 非同期のDBセッション
    """
    await user_services.delete_user(user_me, db)
