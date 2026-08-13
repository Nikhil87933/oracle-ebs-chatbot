from oracle_ebs_chatbot.domain.default_registry import create_default_registry


def test_default_registry_contains_poc_entities() -> None:
    registry = create_default_registry()

    assert registry.get_entity("purchase_order") is not None
    assert registry.get_entity("supplier") is not None


def test_default_registry_contains_poc_metrics() -> None:
    registry = create_default_registry()

    assert registry.get_metric("po_amount") is not None
    assert registry.get_metric("po_count") is not None


def test_default_registry_approves_known_combination() -> None:
    registry = create_default_registry()

    assert registry.is_combination_approved(
        "po_amount",
        {"supplier"},
    )
