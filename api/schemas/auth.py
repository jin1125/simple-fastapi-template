"""Token関連のスキーマ(構造や型)定義ファイル"""
from pydantic import Field

from api.schemas import base


class Token(base.BaseSchema):
    """
    Tokenスキーマ

    - Token本体に定義するスキーマ

    Attributes:
        access_token: アクセストークン
        token_type: トークンタイプ
    """

    access_token: str = Field(description="アクセストークン")
    token_type: str = Field(description="トークンタイプ")
