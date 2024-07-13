"""認証関連のパスオペレーション関数の定義ファイル"""
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.db import get_db
from api.models import user as user_models
from api.schemas import auth as auth_schemas
from api.services import auth as auth_services
from api.settings import constant

router: APIRouter = APIRouter(
    tags=["Auth"],
)


@router.post(
    "/token",
    response_model=auth_schemas.Token,
    summary="トークンを認証",
)
async def authentication_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    """
    トークンを認証

    - ログイン時に利用する

    Args:
    - form_data: 入力されたフォームデータ
    - db: 非同期のDBセッション

    Returns:
    - アクセストークン
    """
    authenticated_user: user_models.User = (
        await auth_services.authenticate_user(form_data, db)
    )
    access_token: str = auth_services.create_access_token(
        authenticated_user.username,
    )
    return {
        "access_token": access_token,
        "token_type": constant.TOKEN_TYPE,
    }
