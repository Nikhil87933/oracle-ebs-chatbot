"""Default governed domain metadata for the POC."""

from oracle_ebs_chatbot.domain.registry import (
    ApprovedCombination,
    Dimension,
    DomainRegistry,
    Entity,
    Metric,
)


def create_default_registry() -> DomainRegistry:
    """Create the governed domain registry used by the POC."""

    purchase_order = Entity(
        name="purchase_order",
        description="A purchase order in Oracle EBS procurement.",
    )

    supplier = Entity(
        name="supplier",
        description="A supplier in Oracle EBS procurement.",
    )

    po_amount = Metric(
        name="po_amount",
        description="Total purchase order amount.",
        entity="purchase_order",
    )

    po_count = Metric(
        name="po_count",
        description="Number of purchase orders.",
        entity="purchase_order",
    )

    supplier_dimension = Dimension(
        name="supplier",
        description="Supplier associated with the purchase order.",
        entity="purchase_order",
    )

    status_dimension = Dimension(
        name="status",
        description="Purchase order status.",
        entity="purchase_order",
    )

    return DomainRegistry(
        entities={
            purchase_order.name: purchase_order,
            supplier.name: supplier,
        },
        metrics={
            po_amount.name: po_amount,
            po_count.name: po_count,
        },
        dimensions={
            supplier_dimension.name: supplier_dimension,
            status_dimension.name: status_dimension,
        },
        approved_combinations=[
            ApprovedCombination(
                metric="po_amount",
                dimensions=frozenset({"supplier"}),
            ),
            ApprovedCombination(
                metric="po_amount",
                dimensions=frozenset({"status"}),
            ),
            ApprovedCombination(
                metric="po_amount",
                dimensions=frozenset({"supplier", "status"}),
            ),
            ApprovedCombination(
                metric="po_count",
                dimensions=frozenset({"supplier"}),
            ),
            ApprovedCombination(
                metric="po_count",
                dimensions=frozenset({"status"}),
            ),
        ],
    )
