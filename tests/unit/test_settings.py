from oracle_ebs_chatbot.config.settings import Settings, get_settings


def test_settings_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.ords_base_url == ""
    assert settings.ords_timeout_seconds == 10.0
    assert settings.ollama_host == "http://localhost:11434"
    assert settings.ollama_model == ""
    assert settings.app_env == "development"
    assert settings.log_level == "INFO"


def test_get_settings_returns_cached_instance() -> None:
    get_settings.cache_clear()

    first = get_settings()
    second = get_settings()

    assert first is second


def test_settings_reads_external_service_configuration(
    monkeypatch,
) -> None:
    from oracle_ebs_chatbot.config.settings import Settings

    monkeypatch.setenv(
        "ORDS_BASE_URL",
        "http://ords-server:8080/ords",
    )
    monkeypatch.setenv(
        "ORDS_TIMEOUT_SECONDS",
        "20",
    )
    monkeypatch.setenv(
        "OLLAMA_HOST",
        "http://ollama-server:11434",
    )
    monkeypatch.setenv(
        "OLLAMA_MODEL",
        "qwen",
    )
    monkeypatch.setenv(
        "CHATBOT_DEFAULT_USERNAME",
        "POC_USER",
    )

    settings = Settings(_env_file=None)

    assert settings.ords_base_url == "http://ords-server:8080/ords"
    assert settings.ords_timeout_seconds == 20.0
    assert settings.ollama_host == "http://ollama-server:11434"
    assert settings.ollama_model == "qwen"
    assert settings.chatbot_default_username == "POC_USER"
