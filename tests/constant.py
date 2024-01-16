"""テスト用の定数の定義ファイル"""
from api.config import settings

TEST_USER_NAME = "test_user_name"
TEST_USER_EMAIL = "test_user_email@test.com"
TEST_USER_PASSWORD = "test_user_password"
TEST_UPDATE_USER_NAME = "update_test_user_name"
TEST_UPDATE_USER_EMAIL = "update_test_user_email@test.com"
TEST_UPDATE_USER_PASSWORD = "update_test_user_password"
TEST_TODO_TITLE = "test_todo_title"
TEST_TODO_DETAIL = "test_todo_detail"
TEST_TODO_DUE_DATE = "2030-01-01"
TEST_UPDATE_TODO_TITLE = "update_test_todo_title"
TEST_UPDATE_TODO_DETAIL = "update_test_todo_detail"
TEST_UPDATE_TODO_DUE_DATE = "2030-12-31"
TEST_UPDATE_DONE = True

ASYNC_TEST_DB_URL = (
    settings.get_async_url()
    .set(
        database=settings.test_postgres_db,
        host=settings.test_postgres_host,
        port=settings.test_postgres_port,
        username=settings.test_postgres_user,
        password=settings.test_postgres_password,
    )
    .render_as_string(hide_password=False)
)
