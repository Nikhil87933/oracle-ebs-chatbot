import json
import logging

from oracle_ebs_chatbot.audit.logger import AuditEvent, AuditLogger


def test_audit_event_defaults() -> None:
    event = AuditEvent(
        request_id="req-123",
        user="SYSADMIN",
        tool="entity_lookup",
        params={"entity": "supplier", "identifier": "1001"},
        result="success",
    )

    assert event.request_id == "req-123"
    assert event.user == "SYSADMIN"
    assert event.tool == "entity_lookup"
    assert event.params["entity"] == "supplier"
    assert event.result == "success"
    assert event.timestamp is not None


def test_audit_event_serializes_to_json() -> None:
    event = AuditEvent(
        request_id="req-123",
        user="SYSADMIN",
        tool="entity_lookup",
        result="success",
    )

    payload = json.loads(event.model_dump_json())

    assert payload["request_id"] == "req-123"
    assert payload["user"] == "SYSADMIN"
    assert payload["tool"] == "entity_lookup"
    assert payload["result"] == "success"
    assert "timestamp" in payload
    assert payload["params"] == {}


def test_audit_logger_emits_event(
    caplog: object,
) -> None:
    logger = logging.getLogger("oracle_ebs_chatbot.audit")
    audit_logger = AuditLogger(logger)

    event = AuditEvent(
        request_id="req-456",
        user="SYSADMIN",
        tool="aggregate_query",
        params={"metric": "po_amount"},
        result="success",
    )

    with caplog.at_level(logging.INFO, logger="oracle_ebs_chatbot.audit"):  # type: ignore[attr-defined]
        audit_logger.log(event)

    assert "req-456" in caplog.text  # type: ignore[attr-defined]
    assert "aggregate_query" in caplog.text  # type: ignore[attr-defined]
    assert "success" in caplog.text  # type: ignore[attr-defined]
