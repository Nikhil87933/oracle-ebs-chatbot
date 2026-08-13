from oracle_ebs_chatbot.config.settings import Settings, get_settings


def test_settings_defaults() -> None:
    settings = Settings()

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
