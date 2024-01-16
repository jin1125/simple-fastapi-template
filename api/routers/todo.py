"""Todo関連のパスオペレーション関数の定義ファイル"""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.db import get_db
from api.models import todo as todo_models
from api.schemas import todo as todo_schemas
from api.schemas import user as user_schemas
from api.services import todo as todo_services
from api.services import user as user_services

router: APIRouter = APIRouter(
    prefix="/todo",
    tags=["Todo"],
)


@router.post(
    "/create",
    response_model=todo_schemas.Todo,
    status_code=201,
    summary="Todoを作成",
)
async def create_todo(
    create_todo_data: todo_schemas.TodoCreate,
    user_me: Annotated[user_schemas.User, Depends(user_services.get_user_me)],
    db: AsyncSession = Depends(get_db),
):
    """
    Todoを作成

    Args:
        create_todo_data: Todoを作成するための情報
        user_me: ログインユーザー
        db: 非同期のDBセッション

    Returns:
        作成したTodo
    """
    return await todo_services.create_todo(create_todo_data, user_me.id, db)


@router.get(
    "/list",
    response_model=list[todo_schemas.Todo],
    summary="Todo一覧を取得",
)
async def read_todo_list(
    user_me: Annotated[user_schemas.User, Depends(user_services.get_user_me)],
    db: AsyncSession = Depends(get_db),
):
    """
    Todo一覧を取得

    Args:
        user_me: ログインユーザー
        db: 非同期のDBセッション

    Returns:
        Todo一覧
    """
    return await todo_services.read_todo_list(user_me.id, db)


@router.get(
    "/detail/{todo_id}",
    response_model=todo_schemas.Todo,
    summary="Todo詳細を取得",
)
async def read_todo_detail(
    todo_id: int,
    user_me: Annotated[user_schemas.User, Depends(user_services.get_user_me)],
    db: AsyncSession = Depends(get_db),
):
    """
    Todo詳細を取得

    Args:
        todo_id: 詳細を取得したいTodoID
        user_me: ログインユーザー
        db: 非同期のDBセッション

    Returns:
        Todo詳細
    """
    return await todo_services.read_todo_detail(todo_id, user_me.id, db)


@router.patch(
    "/update/{todo_id}",
    response_model=todo_schemas.Todo,
    summary="Todoを更新",
)
async def update_todo(
    todo_id: int,
    user_me: Annotated[user_schemas.User, Depends(user_services.get_user_me)],
    update_todo_data: todo_schemas.TodoUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Todoを更新

    Args:
        todo_id: 更新したいTodoID
        user_me: ログインユーザー
        update_todo_data: Todoを更新するための情報
        db: 非同期のDBセッション

    Returns:
        Todo詳細
    """
    target_todo: todo_models.Todo = await todo_services.read_todo_detail(
        todo_id,
        user_me.id,
        db,
    )
    return await todo_services.update_todo(
        target_todo,
        update_todo_data,
        db,
    )


@router.delete(
    "/delete/{todo_id}",
    response_model=None,
    status_code=204,
    summary="Todoを削除",
)
async def delete_todo(
    todo_id: int,
    user_me: Annotated[user_schemas.User, Depends(user_services.get_user_me)],
    db: AsyncSession = Depends(get_db),
):
    """
    Todoを削除

    Args:
        todo_id: 削除したいTodoID
        user_me: ログインユーザー
        db: 非同期のDBセッション
    """
    await todo_services.delete_todo(todo_id, db)
