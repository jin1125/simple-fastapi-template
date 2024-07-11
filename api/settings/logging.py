"""Loggingの設定ファイル"""
import logging


def setup_logging():
    """
    ロギングの設定

    - 出力するログの設定を行う
    """
    logging.basicConfig(
        filename="api/logs/api.log",
        format="[%(levelname)s] %(asctime)s | "
        "%(name)s:%(lineno)d | %(message)s",
        level=logging.INFO,
    )
