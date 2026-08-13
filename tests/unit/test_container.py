from oracle_ebs_chatbot.app.container import create_chat_service
from oracle_ebs_chatbot.chat.service import ChatService
from oracle_ebs_chatbot.config.settings import Settings


def test_create_chat_service() -> None:
    service = create_chat_service(
        Settings(
            ords_base_url="http://mock-ords",
            ollama_host="http://mock-ollama:11434",
            ollama_model="qwen",
        )
    )

    assert isinstance(service, ChatService)


def test_chat_service_dependency_is_cached() -> None:
    from oracle_ebs_chatbot.api.routes_chat import get_chat_service

    get_chat_service.cache_clear()

    first = get_chat_service()
    second = get_chat_service()

    assert first is second

    get_chat_service.cache_clear()
