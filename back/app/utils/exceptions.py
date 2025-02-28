# utils/exceptions.py
from app.utils.errors import ErrorCode


class CustomException(Exception):
    """アプリケーション内で発生するカスタム例外の基底クラス。
    ErrorCode のみを持つシンプルな例外クラス。
    """

    def __init__(self, error_code: ErrorCode, message: str, status_code: int):
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
