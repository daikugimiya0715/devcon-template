# services/vertex_ai.py
from typing import Optional

import vertexai
from google.cloud import aiplatform
from loguru import logger
from vertexai.generative_models import (
    Candidate,
    FinishReason,
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
)

from app.utils.errors import ErrorCode
from app.utils.exceptions import CustomException


class VertexAIClient:
    """Google Cloud Vertex AI の Gemini モデルとやり取りするためのクライアントクラス。

    このクラスは、Vertex AI の Prediction Service API を使用してテキスト生成を行います。
    環境変数からプロジェクト ID、ロケーション、モデル名を取得し、クライアントを初期化します。

    Attributes:
        project_id (str): Google Cloud プロジェクト ID。
        location (str): Vertex AI モデルがデプロイされているリージョン。
        model_name (str): 使用する Vertex AI モデルの名前 (例: "gemini-1.0-pro")。

    """

    def __init__(
        self,
        project_id: str,
        location: str,
        model_name: str,
    ):
        """VertexAIClient のコンストラクタ。

        Args:
            project_id (str, optional): Google Cloud プロジェクト ID. デフォルトは環境変数から取得。
            location (str, optional): Vertex AI モデルのリージョン. デフォルトは環境変数から取得。
            model_name (str, optional): Vertex AI モデル名. デフォルトは環境変数から取得。
        """
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        self.generative_model = GenerativeModel(model_name=model_name)

    def generate_content(self, prompt: str, generation_config: dict | None = None) -> str:
        """Vertex AI の Gemini モデルを使用してテキストを生成する。

        Args:
            prompt (str): ユーザーからの入力テキスト (プロンプト)。
            generation_config (Optional[Dict]): 生成設定

        Returns:
            str: 生成されたテキスト。

        Raises:
            CustomException: Vertex AI API からのエラー、またはレスポンスの形式が不正な場合。

        """
        # Vertex AI クライアントの初期化 (毎回初期化する)
        vertexai.init(project=self.project_id, location=self.location)

        logger.info(f"project_id: {self.project_id}, location: {self.location}, model_name: {self.model_name}")

        if generation_config is None:
            generation_config = {}

        try:
            # テキスト生成の実行
            response = self.generative_model.generate_content(
                prompt,
                generation_config=generation_config,
            )

        except Exception as e:
            logger.error(f"Error during generateContent API call: {e}")
            err_msg = str(e)
            if (
                "PERMISSION_DENIED" in err_msg
                or "Unable to authenticate your request" in err_msg
                or "unable to impersonate" in err_msg
            ):
                if "Unable to authenticate" in err_msg:
                    raise CustomException(ErrorCode.UNAUTHENTICATED, "Authentication failed", 401) from e  # 認証エラー
                raise CustomException(ErrorCode.PERMISSION_DENIED, "Permission Denied", 403) from e  # 権限エラー
            # その他のVertexAI起因のエラー
            raise CustomException(ErrorCode.VERTEX_AI_ERROR, str(e), 500) from e

        # レスポンスの検証
        if not response:
            raise CustomException(ErrorCode.NO_RESPONSE, "No response received from Vertex AI.", 500)
        if response.prompt_feedback:  # プロンプトが不適切でブロックされた場合
            logger.warning(f"Prompt feedback: {response.prompt_feedback}")
            raise CustomException(ErrorCode.INVALID_REQUEST, "Prompt was blocked due to safety concerns.", 400)

        if not response.candidates:
            raise CustomException(
                ErrorCode.NO_CANDIDATE,
                "No candidate responses received from Vertex AI.",
                500,
            )
        # finish_reason (停止理由) を確認
        candidate: Candidate = response.candidates[0]
        if candidate.finish_reason != FinishReason.STOP:
            if candidate.finish_reason == FinishReason.SAFETY:
                raise CustomException(ErrorCode.VERTEX_AI_ERROR, "Candidate was blocked due to safety concerns.", 400)
            logger.warning(f"Candidate finish reason: {candidate.finish_reason}")  # 他の理由の場合はログ出力

        if not candidate.content:
            raise CustomException(ErrorCode.MISSING_CONTENT, "Candidate response is missing content.", 500)

        if not candidate.content.parts:
            raise CustomException(ErrorCode.MISSING_CONTENT, "Candidate response is missing content parts.", 500)

        answer_text = "".join(part.text for part in candidate.content.parts)
        logger.info(f"Generated answer text: {answer_text}")
        return answer_text
