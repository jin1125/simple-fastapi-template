"""ユーザー関連のスキーマ(構造や型)定義ファイル"""
from pydantic import EmailStr, Field

from api.schemas import base


class UserBase(base.BaseSchema):
    """
    ユーザーベーススキーマ

    - ユーザー関連の共通スキーマの定義を行う(継承元)

    Attributes:
        username: ユーザー名
        email: メールアドレス
    """

    username: str = Field(description="ユーザー名")
    email: EmailStr = Field(description="メールアドレス")


class UserCreate(UserBase):
    """
    ユーザー作成スキーマ

    - ユーザーの作成時に定義するスキーマ

    Attributes:
        password: パスワード

    Note:
        UserBaseクラスを継承
    """

    password: str = Field(description="パスワード")


class UserStore(UserBase):
    """
    ユーザー保存スキーマ

    - ユーザーのDB保存時に定義するスキーマ

    Attributes:
        hashed_password: ハッシュ化パスワード

    Note:
        UserBaseクラスを継承
    """

    hashed_password: str = Field(description="ハッシュ化パスワード")


class UserUpdate(base.BaseSchema):
    """
    ユーザー更新スキーマ

    - ユーザーの更新時に定義するスキーマ

    Attributes:
        password: パスワード

    Note:
        UserBaseクラスを継承
    """

    username: str | None = Field(default=None, description="ユーザー名")
    email: EmailStr | None = Field(default=None, description="メールアドレス")
    password: str | None = Field(default=None, description="パスワード")


class User(UserBase):
    """
    ユーザースキーマ

    - ユーザー本体に定義するスキーマ

    Attributes:
        id: ID
        hashed_password: ハッシュ化パスワード

    Note:
        UserBaseクラスを継承
    """

    id: int = Field(description="ID", ge=1)
    hashed_password: str = Field(description="ハッシュ化パスワード")
