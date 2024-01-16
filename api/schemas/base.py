"""共通のスキーマ(構造や型)定義ファイル"""
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    ベーススキーマ

    - 全スキーマで共通の定義を行う(継承元)

    Attributes:
        model_config: Pydanticモデルの設定
    """

    model_config = ConfigDict(from_attributes=True)
