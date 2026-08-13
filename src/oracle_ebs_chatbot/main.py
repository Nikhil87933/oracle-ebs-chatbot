"""FastAPI application entrypoint."""

from fastapi import FastAPI

from oracle_ebs_chatbot.api.routes_chat import router as chat_router
from oracle_ebs_chatbot.api.routes_health import router as health_router

app = FastAPI(
    title="Oracle EBS Chatbot",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(chat_router)
