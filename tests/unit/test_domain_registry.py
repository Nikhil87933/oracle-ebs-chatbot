import pytest

from oracle_ebs_chatbot.domain.registry import (
    ApprovedCombination,
    Dimension,
    DomainRegistry,
    Entity,
    Metric,
)


def test_entity_definition() -> None:
    entity = Entity(
        name="purchase_order",
        description="A purchase order created in Oracle EBS.",
    )

    assert entity.name == "purchase_order"
    assert entity.description == "A purchase order created in Oracle EBS."


def test_metric_definition() -> None:
    metric = Metric(
        name="po_amount",
        description="Total purchase order amount.",
        entity="purchase_order",
    )

    assert metric.name == "po_amount"
    assert metric.entity == "purchase_order"


def test_dimension_definition() -> None:
    dimension = Dimension(
        name="supplier",
        description="Supplier associated with a purchase order.",
        entity="purchase_order",
    )

    assert dimension.name == "supplier"
    assert dimension.entity == "purchase_order"


def test_registry_lookup() -> None:
    entity = Entity(
        name="purchase_order",
        description="A purchase order created in Oracle EBS.",
    )
    metric = Metric(
        name="po_amount",
        description="Total purchase order amount.",
        entity="purchase_order",
    )
    dimension = Dimension(
        name="supplier",
        description="Supplier associated with a purchase order.",
        entity="purchase_order",
    )

    registry = DomainRegistry(
        entities={entity.name: entity},
        metrics={metric.name: metric},
        dimensions={dimension.name: dimension},
    )

    assert registry.get_entity("purchase_order") == entity
    assert registry.get_metric("po_amount") == metric
    assert registry.get_dimension("supplier") == dimension


def test_registry_returns_none_for_unknown_metadata() -> None:
    registry = DomainRegistry()

    assert registry.get_entity("unknown") is None
    assert registry.get_metric("unknown") is None
    assert registry.get_dimension("unknown") is None


def test_approved_combination_is_allowed() -> None:
    entity = Entity(
        name="purchase_order",
        description="A purchase order.",
    )
    metric = Metric(
        name="po_amount",
        description="Total purchase order amount.",
        entity="purchase_order",
    )
    dimension = Dimension(
        name="supplier",
        description="Supplier.",
        entity="purchase_order",
    )

    registry = DomainRegistry(
        entities={"purchase_order": entity},
        metrics={"po_amount": metric},
        dimensions={"supplier": dimension},
        approved_combinations=[
            ApprovedCombination(
                metric="po_amount",
                dimensions=frozenset({"supplier"}),
            )
        ],
    )

    assert registry.is_combination_approved(
        "po_amount",
        {"supplier"},
    )


def test_unapproved_combination_is_rejected() -> None:
    entity = Entity(
        name="purchase_order",
        description="A purchase order.",
    )
    metric = Metric(
        name="po_amount",
        description="Total purchase order amount.",
        entity="purchase_order",
    )
    dimension = Dimension(
        name="supplier",
        description="Supplier.",
        entity="purchase_order",
    )

    registry = DomainRegistry(
        entities={"purchase_order": entity},
        metrics={"po_amount": metric},
        dimensions={"supplier": dimension},
        approved_combinations=[
            ApprovedCombination(
                metric="po_amount",
                dimensions=frozenset({"supplier"}),
            )
        ],
    )

    assert not registry.is_combination_approved(
        "po_amount",
        {"organization"},
    )


def test_dimension_order_does_not_matter() -> None:
    entity = Entity(
        name="purchase_order",
        description="A purchase order.",
    )
    metric = Metric(
        name="po_amount",
        description="Total purchase order amount.",
        entity="purchase_order",
    )
    supplier = Dimension(
        name="supplier",
        description="Supplier.",
        entity="purchase_order",
    )
    organization = Dimension(
        name="organization",
        description="Operating organization.",
        entity="purchase_order",
    )

    registry = DomainRegistry(
        entities={"purchase_order": entity},
        metrics={"po_amount": metric},
        dimensions={
            "supplier": supplier,
            "organization": organization,
        },
        approved_combinations=[
            ApprovedCombination(
                metric="po_amount",
                dimensions=frozenset({"supplier", "organization"}),
            )
        ],
    )

    assert registry.is_combination_approved(
        "po_amount",
        {"organization", "supplier"},
    )


def test_metric_must_reference_existing_entity() -> None:
    with pytest.raises(
        ValueError,
        match="references unknown entity",
    ):
        DomainRegistry(
            metrics={
                "po_amount": Metric(
                    name="po_amount",
                    description="Total purchase order amount.",
                    entity="purchase_order",
                )
            }
        )


def test_dimension_must_reference_existing_entity() -> None:
    with pytest.raises(
        ValueError,
        match="references unknown entity",
    ):
        DomainRegistry(
            dimensions={
                "supplier": Dimension(
                    name="supplier",
                    description="Supplier.",
                    entity="purchase_order",
                )
            }
        )


def test_combination_must_reference_existing_metric() -> None:
    with pytest.raises(
        ValueError,
        match="unknown metric",
    ):
        DomainRegistry(
            approved_combinations=[
                ApprovedCombination(
                    metric="po_amount",
                    dimensions=frozenset(),
                )
            ]
        )


def test_combination_must_reference_existing_dimension() -> None:
    entity = Entity(
        name="purchase_order",
        description="A purchase order.",
    )
    metric = Metric(
        name="po_amount",
        description="Total purchase order amount.",
        entity="purchase_order",
    )

    with pytest.raises(
        ValueError,
        match="unknown dimension",
    ):
        DomainRegistry(
            entities={"purchase_order": entity},
            metrics={"po_amount": metric},
            approved_combinations=[
                ApprovedCombination(
                    metric="po_amount",
                    dimensions=frozenset({"supplier"}),
                )
            ],
        )
