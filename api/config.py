"""環境変数の読み込みファイル"""
from functools import lru_cache

import sqlalchemy
from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    """
    環境変数を.envから読み込む

    - .envファイルに定義されている環境変数を読み込む
    - 環境変数が定義されていない場合、クラス変数が使用される

    Attributes:
        access_token_expire_minutes: アクセストークンの有効時間(分)
        algorithm: jwtの署名で使用するアルゴリズム
        app_title: アプリのタイトル
        cors_credentials: CORS設定のCookieの共有を許可するかどうか
        cors_headers: CORS設定のクロスオリジンリクエストに対応するHTTPリクエストヘッダのリスト
        cors_methods: CORS設定のクロスオリジンリクエストを許可するHTTPメソッドのリスト
        cors_origins: CORS設定のクロスオリジンリクエストを許可するオリジンのリスト
        db_echo: SQLのログを出力するかどうか
        db_port: DBのポート番号
        docs_url: SwaggerUIのURL設定
        postgres_db: PostgreSQLのデータベース名
        postgres_alembic_host: PostgreSQLのalembicでのホスト名
        postgres_host: PostgreSQLのホスト名
        postgres_password: PostgreSQLのパスワード
        postgres_port: PostgreSQLのポート番号
        postgres_user: PostgreSQLのユーザ名
        test_db_echo: テスト時にSQLのログを出力するかどうか
        test_postgres_db: テスト用のPostgreSQLのデータベース名
        test_postgres_host: テスト用のPostgreSQLのホスト名
        test_postgres_password: テスト用のPostgreSQLのパスワード
        test_postgres_port: テスト用のPostgreSQLのポート番号
        test_postgres_user: テスト用のPostgreSQLのユーザ名
        redoc_url: ReDocのURL設定
        secret_key: jwtで使用するアルゴリズムに適したキー
        token_url: OAuth2PasswordBearerのtokenUrlパラメータに定義するURL

        model_config: クラスの設定を定義
    """

    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    app_title: str = "Todo App"
    cors_credentials: bool = True
    cors_headers: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_origins: list[str] = ["*"]
    db_echo: bool = False
    db_port: int = 5432
    docs_url: str | None = "/docs"
    postgres_db: str = "postgres"
    postgres_alembic_host: str = "localhost"
    postgres_host: str = "db"
    postgres_password: str = "postgres"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    test_db_echo: bool = False
    test_postgres_db: str = "test_db"
    test_postgres_host: str = "test-db"
    test_postgres_password: str = "password"
    test_postgres_port: int = 5432
    test_postgres_user: str = "test_user"
    redoc_url: str | None = "/redoc"
    secret_key: str = ""
    token_url: str = "token"

    def get_async_url(self) -> URL:
        """
        PostgreSQLへの非同期接続情報(URL)を取得

        - URLを生成

        Returns:
            PostgreSQLへの非同期接続情報(URL)
        """
        return sqlalchemy.engine.url.URL.create(
            drivername="postgresql+asyncpg",
            database=self.postgres_db,
            host=self.postgres_host,
            port=self.postgres_port,
            username=self.postgres_user,
            password=self.postgres_password,
        )

    def get_oauth2_scheme(self) -> OAuth2PasswordBearer:
        """
        認証用のトークンを取得

        - OAuth2PasswordBearerクラスをインスタンス化
        - 「username」と「password」を送信するための、tokenUrlパラメータのURLを定義する
        - tokenUrlに値を送信して、認証用のトークンを取得する

        Returns:
            OAuth2PasswordBearerクラスのインスタンス
        """
        return OAuth2PasswordBearer(tokenUrl=self.token_url)

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_settings() -> Settings:
    """
    環境変数もしくはクラス変数を取得

    - .envの環境変数もしくはSettingsクラス変数を取得する
    - lru_cacheデコレータによって、Settingsクラスは1度だけインスタンス化される

    Returns:
        Settingsクラスのインスタンス
    """
    return Settings()


settings: Settings = get_settings()
