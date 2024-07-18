"""ユーザー関連の関数定義ファイル"""
import logging
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import settings
from api.database.db import get_db
from api.exceptions import status_4xx
from api.models import user as user_models
from api.schemas import user as user_schemas
from api.services import auth as auth_services

logger: logging.Logger = logging.getLogger(__name__)


async def create_user(
    create_user_data: user_schemas.UserCreate,
    db: AsyncSession,
) -> user_models.User | None:
    """
    ユーザーを作成

    - パスワードをハッシュ化して、ユーザーを作成する

    Args:
    - create_user_data: ユーザーを作成するための情報
    - db: 非同期のDBセッション

    Returns:
    - 作成したユーザー
    """
    hashed_password: str = auth_services.get_hashed_password(
        create_user_data.password
    )
    user_schema: user_schemas.UserStore = user_schemas.UserStore(
        **create_user_data.model_dump(),
        hashed_password=hashed_password,
    )
    stmt = (
        insert(user_models.User)
        .values(
            **user_schema.model_dump(),
        )
        .returning(user_models.User)
    )
    return await db.scalar(stmt)


async def get_user_me(
    token: Annotated[str, Depends(settings.get_oauth2_scheme())],
    db: AsyncSession = Depends(get_db),
) -> user_models.User:
    """
    ログインユーザーを取得

    Args:
    - token: 認証用のトークン
    - db: 非同期のDBセッション

    Returns:
    - ログインユーザー
    """
    payload: dict[str, Any] = auth_services.get_decode_jwt(token)
    username: Any | None = payload.get("sub")
    if username is None:
        logger.error("ペイロードのsubを取得できませんでした")
        raise status_4xx.UnauthorizedException(
            None,
            {"WWW-Authenticate": "Bearer"},
        )
    return await auth_services.get_user_by_user_name(username, db)


async def update_user(
    user_me: user_models.User,
    update_user_data: user_schemas.UserUpdate,
    db: AsyncSession,
) -> user_models.User | None:
    """
    ログインユーザーを更新

    - 部分更新が可能

    Args:
    - user_me: 更新したいログインユーザーモデル
    - update_user_data: ログインユーザーを更新するための情報
    - db: 非同期のDBセッション

    Returns:
    - 更新したユーザー
    """
    update_data: dict = update_user_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = auth_services.get_hashed_password(
            update_data["password"]
        )
        del update_data["password"]

    stmt = (
        update(user_models.User)
        .where(user_models.User.id == user_me.id)
        .values(**update_data)
        .returning(user_models.User)
    )
    return await db.scalar(stmt)


async def delete_user(
    user_me: user_models.User,
    db: AsyncSession,
) -> None:
    """
    ログインユーザーを削除

    Args:
    - user_me: 削除したいログインユーザーモデル
    - db: 非同期のDBセッション
    """
    stmt = delete(user_models.User).where(user_models.User.id == user_me.id)
    await db.execute(stmt)
