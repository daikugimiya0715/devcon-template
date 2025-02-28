# utils/errors.py
from enum import Enum


class ErrorCode(str, Enum):
    """Enum class for error codes."""

    # 認証関連のエラー
    UNAUTHENTICATED = "UNAUTHENTICATED"  # 認証エラー
    PERMISSION_DENIED = "PERMISSION_DENIED"  # 権限不足

    # リクエスト関連のエラー
    INVALID_REQUEST = "INVALID_REQUEST"  # 無効なリクエスト
    MISSING_PROMPT = "MISSING_PROMPT"  # プロンプトがない（必要に応じて）
    VALIDATION_ERROR = "VALIDATION_ERROR"  # 入力検証エラー

    # Vertex AI 関連のエラー
    VERTEX_AI_ERROR = "VERTEX_AI_ERROR"  # Vertex AI API エラー
    NO_RESPONSE = "NO_RESPONSE"  # Vertex AI からの応答がない
    NO_CANDIDATE = "NO_CANDIDATE"  # Vertex AI からの候補がない
    MISSING_CONTENT = "MISSING_CONTENT"  # Vertex AI からのコンテンツがない

    # 内部エラー
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"  # 内部サーバーエラー
