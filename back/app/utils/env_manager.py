# utils/env_manager.py
import os
from typing import Optional

from loguru import logger
from pydantic import BaseModel, Field, ValidationError, field_validator


class EnvironmentVariables(BaseModel):
    """Class for managing environment variables required for Vertex AI integration.

    This class validates and manages essential environment variables needed for
    interacting with Google Cloud's Vertex AI services. It uses Pydantic for
    validation and provides methods to load configurations from environment variables.

    Attributes:
        PROJECT_ID (str): The Google Cloud project identifier.
        LOCATION (str): The geographical region where Vertex AI model is deployed.
        TEXT_MODEL (str): The name of the Vertex AI model to use, defaults to "gemini-1.0-pro".
        EMPTY_ENV_ERROR (str): Error message for empty environment variables.

    Raises:
        ValidationError: If any required environment variable is empty or invalid.
    """

    PROJECT_ID: str = Field(..., description="Google Cloud project ID.")
    LOCATION: str = Field(..., description="Vertex AI model deployment region.")
    TEXT_MODEL: str = Field("gemini-1.0-pro", description="Vertex AI model name.")

    @field_validator("PROJECT_ID", "LOCATION", mode="before")
    @classmethod
    def check_not_empty(cls, v: str) -> str:  # noqa: D102
        if not v:
            raise ValidationError("Environment variable must not be empty")
        return v

    @classmethod
    def from_env(cls) -> "EnvironmentVariables":
        """環境変数から設定を読み込み、EnvironmentVariables オブジェクトを返す."""
        try:
            return cls(
                PROJECT_ID=os.environ.get("PROJECT_ID", "PROJECT_ID_NOT_SET"),
                LOCATION=os.environ.get("LOCATION", "LOCATION_NOT_SET"),
                TEXT_MODEL=os.environ.get("TEXT_MODEL", "gemini-1.0-pro"),
            )
        except ValidationError as e:
            logger.error(f"Environment variable validation error: {e}")
            raise  # エラーを上位に伝播


# env_vars を関数内で初期化するように変更
def get_env_vars() -> EnvironmentVariables:
    return EnvironmentVariables.from_env()
