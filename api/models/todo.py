"""Todoモデルの定義ファイル"""
import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.db import Base

if TYPE_CHECKING:
    from api.models import user as user_models


class Todo(Base):
    """
    Todoモデル

    - DBのテーブルを表すSQLAlchemy(ORM)モデルを定義

    Attributes:
        __tablename__: テーブル名を定義
        id: IDのカラム
        detail: 詳細のカラム
        due_date: 期限のカラム
        done: 完了フラグのカラム
        user_id: ユーザーIDのカラム(外部キー)
        user: usersテーブルと関連付けするように指定
    """

    __tablename__: str = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="ID")
    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        comment="タイトル",
    )
    detail: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
        comment="詳細",
    )
    due_date: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=False,
        comment="期限",
    )
    done: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="完了フラグ",
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        comment="ユーザーID",
    )

    user: Mapped["user_models.User"] = relationship(
        "User",
        back_populates="todos",
    )
