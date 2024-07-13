"""Todo関連のスキーマ(構造や型)定義ファイル"""
import datetime

from pydantic import Field

from api.schemas import base


class TodoBase(base.BaseSchema):
    """
    Todoベーススキーマ

    - Todo関連の共通スキーマの定義を行う(継承元)

    Attributes:
        title: タイトルのフィールド
        detail: 詳細のフィールド
        due_date: 期限のフィールド
    """

    title: str = Field(description="タイトル")
    detail: str = Field(description="詳細")
    due_date: datetime.date = Field(description="期限")


class TodoCreate(TodoBase):
    """
    Todo作成スキーマ

    - Todoの作成時に定義するスキーマ

    Note:
        TodoBaseクラスを継承
    """

    pass


class TodoUpdate(base.BaseSchema):
    """
    Todo更新スキーマ

    - Todoの更新時に定義するスキーマ

    Attributes:
        title: タイトルのフィールド
        detail: 詳細のフィールド
        due_date: 期限のフィールド
        done: 完了フラグのフィールド

    Note:
        TodoBaseクラスを継承
    """

    title: str | None = Field(default=None, description="タイトル")
    detail: str | None = Field(default=None, description="詳細")
    due_date: datetime.date | None = Field(default=None, description="期限")
    done: bool | None = Field(default=None, description="完了フラグ")


class Todo(TodoBase):
    """
    Todoスキーマ

    - Todo本体に定義するスキーマ

    Attributes:
        id: IDのフィールド
        done: 完了フラグのフィールド
        user_id: ユーザーID(外部キー)のフィールド

    Note:
        TodoBaseクラスを継承
    """

    id: int = Field(description="ID", ge=1)
    done: bool = Field(description="完了フラグ")
    user_id: int = Field(description="ユーザーID", ge=1)
