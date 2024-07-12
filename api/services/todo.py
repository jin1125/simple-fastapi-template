"""Todo関連の関数定義ファイル"""
import logging
from typing import Sequence

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import status_4xx
from api.models import todo as todo_models
from api.schemas import todo as todo_schemas

logger: logging.Logger = logging.getLogger(__name__)


async def create_todo(
    create_todo_data: todo_schemas.TodoCreate,
    user_id: int,
    db: AsyncSession,
) -> todo_models.Todo | None:
    """
    Todoを作成

    - ログインユーザーのTodoを作成する

    Args:
        create_todo_data: Todoを作成するための情報
        user_id: ユーザーID
        db: 非同期のDBセッション

    Returns:
        作成したTodo
    """
    stmt = (
        insert(todo_models.Todo)
        .values(
            **create_todo_data.model_dump(),
            user_id=user_id,
        )
        .returning(todo_models.Todo)
    )
    return await db.scalar(stmt)


async def read_todo_list(
    user_id: int,
    db: AsyncSession,
) -> Sequence[todo_models.Todo]:
    """
    Todo一覧を取得

    - ログインユーザーのTodo一覧を取得する

    Args:
        user_id: ユーザーID
        db: 非同期のDBセッション

    Returns:
        Todo一覧
    """
    stmt = select(todo_models.Todo).where(todo_models.Todo.user_id == user_id)
    result = await db.scalars(stmt)
    return result.all()


async def read_todo_detail(
    todo_id: int,
    user_id: int,
    db: AsyncSession,
) -> todo_models.Todo:
    """
    Todo詳細を取得

    - ログインユーザーのTodo詳細を取得する

    Args:
        todo_id: TodoID
        user_id: ユーザーID
        db: 非同期のDBセッション

    Returns:
        Todo詳細
    """
    stmt = select(todo_models.Todo).where(
        todo_models.Todo.user_id == user_id,
        todo_models.Todo.id == todo_id,
    )
    todo: todo_models.Todo | None = await db.scalar(stmt)
    if todo is None:
        logger.error("Todoを取得できませんでした")
        raise status_4xx.NotFoundException
    return todo


async def update_todo(
    target_todo: todo_models.Todo,
    update_todo_data: todo_schemas.TodoUpdate,
    db: AsyncSession,
) -> todo_models.Todo | None:
    """
    Todoを更新

    - ログインユーザーのTodoを更新する
    - 部分更新が可能

    Args:
        target_todo: 更新したいTodoモデル
        update_todo_data: Todoを更新するための情報
        db: 非同期のDBセッション

    Returns:
        更新したTodo
    """
    stmt = (
        update(todo_models.Todo)
        .where(todo_models.Todo.id == target_todo.id)
        .values(**update_todo_data.model_dump(exclude_unset=True))
        .returning(todo_models.Todo)
    )
    return await db.scalar(stmt)


async def delete_todo(
    todo_id: int,
    db: AsyncSession,
) -> None:
    """
    Todoを削除

    - ログインユーザーのTodoを削除する

    Args:
        todo_id: 削除したいTodoのID
        db: 非同期のDBセッション
    """
    stmt = delete(todo_models.Todo).where(todo_models.Todo.id == todo_id)
    await db.execute(stmt)
