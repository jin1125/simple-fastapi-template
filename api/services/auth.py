"""認証関連の関数定義ファイル"""
import logging
from datetime import datetime, timedelta
from typing import Any

from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import settings
from api.exceptions import status_4xx
from api.models import user as user_models
from api.settings import constant

logger: logging.Logger = logging.getLogger(__name__)

pwd_context: CryptContext = CryptContext(
    schemes=constant.CRYPT_CONTEXT_SCHEMES,
    deprecated=constant.CRYPT_CONTEXT_DEPRECATED,
)


def get_hashed_password(plain_password: str) -> str:
    """
    ハッシュ化パスワードを取得

    - プレーンパスワードをハッシュ化する

    Args:
    - plain_password: プレーンパスワード

    Returns:
    - ハッシュ化パスワード
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    パスワードを認証

    - プレーンパスワードとハッシュ化パスワードが一致するか確認

    Args:
    - plain_password: プレーンパスワード
    - hashed_password: ハッシュ化パスワード

    Returns:
    - True/False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_encode_jwt(payload: dict[str, str | datetime]) -> str:
    """
    トークンを生成(トークンをエンコード)

    - 以下の情報をもとに、エンコード(符号化)してトークンを生成する
        - ペイロード
        - トークンを署名するための秘密鍵
        - トークンを署名するためのアルゴリズム

    Args:
    - payload: エンコード(符号化)したいデータ

    Returns:
    - アクセストークン
    """
    try:
        access_token = jwt.encode(
            payload,
            settings.secret_key,
            algorithm=settings.algorithm,
        )
    except JWTError:
        logger.error("トークンの生成に失敗しました")
        raise status_4xx.UnauthorizedException(
            None,
            {"WWW-Authenticate": "Bearer"},
        )
    return access_token


def get_decode_jwt(token: str) -> dict[str, Any]:
    """
    ペイロードを取得(トークンをデコード)

    - 以下の情報をもとに、デコード(復号化)してペイロードを取得する
        - トークン
        - トークンを署名した秘密鍵
        - トークンを署名したアルゴリズム

    Args:
    - token: デコード(復号化)したいトークン

    Returns:
    - ペイロード
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=settings.algorithm,
        )
    except JWTError:
        logger.error("ペイロードの取得に失敗しました")
        raise status_4xx.UnauthorizedException(
            None,
            {"WWW-Authenticate": "Bearer"},
        )
    return payload


async def get_user_by_user_name(
    username: str,
    db: AsyncSession,
) -> user_models.User:
    """
    ユーザーをユーザー名で取得

    - DBに対象のユーザー名のユーザーが存在するか検索
    - 存在した場合は、ユーザーを取得

    Args:
    - username: ユーザー名
    - db: 非同期のDBセッション

    Returns:
    - ユーザーモデル
    """
    stmt = select(user_models.User).where(
        user_models.User.username == username
    )
    user: user_models.User | None = await db.scalar(stmt)
    if user is None:
        logger.error("ユーザーの取得に失敗しました")
        raise status_4xx.UnauthorizedException(
            None,
            {"WWW-Authenticate": "Bearer"},
        )
    return user


async def authenticate_user(
    form_data: OAuth2PasswordRequestForm,
    db: AsyncSession,
) -> user_models.User:
    """
    ユーザー認証を行い、ログインユーザーを取得

    - 入力されたフォームデータでユーザー認証を行う
        - ユーザー名
        - パスワード
    - 認証できた場合、対象のユーザーを取得する

    Args:
    - form_data: 入力されたフォームデータ
    - db: 非同期のDBセッション

    Returns:
    - ログインユーザーモデル
    """
    authenticated_user: user_models.User = await get_user_by_user_name(
        form_data.username,
        db,
    )

    is_verify_password = verify_password(
        form_data.password,
        authenticated_user.hashed_password,
    )
    if not is_verify_password:
        logger.error("パスワードの認証に失敗しました")
        raise status_4xx.UnauthorizedException(
            None,
            {"WWW-Authenticate": "Bearer"},
        )
    return authenticated_user


def create_access_token(username: str) -> str:
    """
    アクセストークンを生成

    - ペイロードを定義する
        - ユーザー名
        - トークンの有効期限
    - ペイロードをもとに、アクセストークンを生成する

    Args:
    - username: 認証されたユーザー名

    Returns:
    - アクセストークン
    """
    access_token_expires: datetime = datetime.now() + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload: dict[str, str | datetime] = {
        "sub": username,
        "exp": access_token_expires,
    }
    return get_encode_jwt(payload)
