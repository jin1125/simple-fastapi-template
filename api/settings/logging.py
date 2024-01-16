"""Loggingの設定ファイル"""
import logging

from api.settings.constant import BASE_PATH


def setup_logging():
    """
    ロギングの設定

    - 出力するログの設定を行う
    """
    logging.basicConfig(
        filename=BASE_PATH / "logs/api.log",
        format="[%(levelname)s] %(asctime)s | "
        "%(name)s:%(lineno)d | %(message)s",
        level=logging.INFO,
    )
