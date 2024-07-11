"""定数の定義ファイル"""
TAGS_METADATA: list[dict[str, str]] = [
    {
        "name": "Auth",
        "description": "認証関連のAPI",
    },
    {
        "name": "User",
        "description": "ユーザー関連のAPI",
    },
    {
        "name": "Todo",
        "description": "Todo関連のAPI",
    },
]

CRYPT_CONTEXT_SCHEMES: list[str] = ["bcrypt"]
CRYPT_CONTEXT_DEPRECATED: str = "auto"

TOKEN_TYPE: str = "bearer"
