# Standard Library
import sys

# Third Party Library
from loguru import logger


# loggerの設定
def configure_logger() -> None:
    """Configures the logger with specific settings.

    This function clears any existing logger configuration and sets up a new
    configuration that outputs logs in JSON format to the terminal. The logs
    include detailed stack traces and error diagnostics, and the log level is
    set to DEBUG or higher.

    The log format includes the timestamp, log level, and message.

    Returns:
        None
    """
    # loggerの初期設定をクリア
    logger.remove()

    # JSON形式でログをターミナルに出力
    logger.add(
        sys.stdout,  # 標準出力にログを出力
        format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}",
        serialize=False,  # JSON形式に設定
        level="DEBUG",  # ログレベルをDEBUG以上に設定
        backtrace=True,  # スタックトレースを詳細に出力
        diagnose=True,  # エラー内容を詳細に出力
    )


# 最初に一度だけ設定を適用する

# `logger` はエクスポートされ、他のモジュールで使用できる
