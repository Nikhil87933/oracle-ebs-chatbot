"""Application dependency composition."""

from oracle_ebs_chatbot.chat.service import ChatService
from oracle_ebs_chatbot.clients.ords_client import OrdsClient
from oracle_ebs_chatbot.config.settings import Settings
from oracle_ebs_chatbot.domain.default_registry import create_default_registry
from oracle_ebs_chatbot.llm.ollama_client import OllamaClient
from oracle_ebs_chatbot.llm.response_parser import LlmResponseParser
from oracle_ebs_chatbot.llm.service import LlmService
from oracle_ebs_chatbot.orchestrator.loop import OrchestratorLoop
from oracle_ebs_chatbot.orchestrator.tool_catalog import ToolCatalog
from oracle_ebs_chatbot.security.auth import AuthenticationService
from oracle_ebs_chatbot.security.authorization import AuthorizationService
from oracle_ebs_chatbot.security.boundary import SecurityBoundary


def create_chat_service(settings: Settings) -> ChatService:
    """Create the fully configured chatbot service."""

    ords_client = OrdsClient(
        base_url=settings.ords_base_url,
        timeout=settings.ords_timeout_seconds,
    )

    domain_registry = create_default_registry()

    ollama_client = OllamaClient(
        host=settings.ollama_host,
        model=settings.ollama_model,
    )

    llm_service = LlmService(
        client=ollama_client,
        parser=LlmResponseParser(),
        domain_registry=domain_registry,
    )

    tool_catalog = ToolCatalog(
        ords_client=ords_client,
        domain_registry=domain_registry,
    )

    orchestrator = OrchestratorLoop(tool_catalog)

    security_boundary = SecurityBoundary(
        authentication=AuthenticationService(),
        authorization=AuthorizationService(
            allowed_capabilities={"chat"},
        ),
    )

    return ChatService(
        llm_service=llm_service,
        orchestrator=orchestrator,
        security_boundary=security_boundary,
    )
