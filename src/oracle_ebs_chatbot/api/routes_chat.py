"""Chat API route."""

from functools import lru_cache

from fastapi import APIRouter

from oracle_ebs_chatbot.api.schemas import ChatRequest, ChatResponse
from oracle_ebs_chatbot.app.container import create_chat_service
from oracle_ebs_chatbot.chat.service import ChatService
from oracle_ebs_chatbot.config.settings import get_settings

router = APIRouter()


@lru_cache
def get_chat_service() -> ChatService:
    """Return the cached application chat service."""
    return create_chat_service(get_settings())


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Process a user chat request."""

    settings = get_settings()
    service = get_chat_service()

    identity = {
        "username": settings.chatbot_default_username,
    }

    result = service.handle_message(
        message=request.message,
        identity=identity,
    )

    return ChatResponse(
        success=result.success,
        data=result.data,
        error=result.error,
    )
