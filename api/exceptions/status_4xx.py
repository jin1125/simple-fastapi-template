"""ステータスコード4xxの例外エラー定義ファイル"""
from typing import Any

from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    """401 Unauthorized"""

    def __init__(
        self,
        detail: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        インスタンスメソッド

        - 初期化しなくても使用可能
            - raise UnauthorizedException
        - レスポンス情報を変更したい場合には引数として渡す
        - detailがNoneの場合は、継承元クラスのデフォルト値が使用される

        Args:
            detail: レスポンスボディのエラー詳細情報
            headers: レスポンスヘッダーの追加情報
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
        )


class NotFoundException(HTTPException):
    """404 NotFound"""

    def __init__(
        self,
        detail: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        インスタンスメソッド

        - 初期化しなくても使用可能
            - raise UnauthorizedException
        - レスポンス情報を変更したい場合には引数として渡す
        - detailがNoneの場合は、継承元クラスのデフォルト値が使用される

        Args:
            detail: レスポンスボディのエラー詳細情報
            headers: レスポンスヘッダーの追加情報
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers=headers,
        )
