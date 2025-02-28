# routers/llm.py
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.schemas.schemas import ErrorResponse, LLMInfo, TextInput, TextOutput
from app.services.vertex_ai import (
    VertexAIClient,
)  # services/vertex_ai.py からインポート
from app.utils.env_manager import get_env_vars
from app.utils.errors import ErrorCode
from app.utils.exceptions import CustomException

router = APIRouter()


# Vertex AI クライアントの初期化 (依存性注入で毎回インスタンス化)
def get_vertex_ai_client() -> VertexAIClient:
    """Create a Vertex AI client instance for generating text."""
    env_vars = get_env_vars()
    return VertexAIClient(
        project_id=env_vars.PROJECT_ID,
        location=env_vars.LOCATION,
        model_name=env_vars.TEXT_MODEL,
    )


@router.post(
    "/llm",
    response_model=TextOutput,
    responses={  # responses を適切に設定
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Generate text using Vertex AI Gemini model.",
    description="Sends a text prompt to the Vertex AI Gemini model and returns the generated text.",
)
async def generate_text(
    text_input: TextInput,
):
    logger.info(f"Incoming request to /llm: {text_input.prompt}")
    try:
        vertex_ai_client: VertexAIClient = get_vertex_ai_client()

        logger.info(f"vertex_ai_client: {vertex_ai_client}")

        answer = vertex_ai_client.generate_content(
            prompt=text_input.prompt,
        )
        return TextOutput(answer=answer)

    except CustomException as e:
        logger.error(f"Error in /llm endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=e.status_code, detail=ErrorResponse(error=e.error_code, message=e.message).dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error in /llm endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(error=ErrorCode.INTERNAL_SERVER_ERROR, message=str(e)).dict(),
        )


@router.get(
    "/llm",
    response_model=LLMInfo,
    summary="Endpoint usage information.",
    description="Provides instructions on how to use the /llm endpoint.",
)
async def get_llm_info():
    try:
        env_vars = get_env_vars()
        return LLMInfo(
            project_id=env_vars.PROJECT_ID,
            location=env_vars.LOCATION,
            text_model=env_vars.TEXT_MODEL,
        )

    except Exception as e:
        logger.error(f"Error in /llm endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
