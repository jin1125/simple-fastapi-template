"""ユーザーモデルの定義ファイル"""
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.db import Base

if TYPE_CHECKING:
    from api.models import todo as todo_models


class User(Base):
    """
    ユーザーモデル

    - DBのテーブルを表すSQLAlchemy(ORM)モデルを定義

    Attributes:
    - __tablename__: テーブル名を定義

    - id: IDのカラム
    - username: ユーザー名のカラム
    - email: メールアドレスのカラム
    - hashed_password: ハッシュ化パスワードのカラム
    - todos: todosテーブルと関連付けするように指定
    """

    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="ID")
    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="ユーザー名",
    )
    email: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        comment="メールアドレス",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(72),
        nullable=False,
        comment="ハッシュ化パスワード",
    )

    todos: Mapped[list["todo_models.Todo"]] = relationship(
        "Todo",
        back_populates="user",
        cascade="delete",
    )
