"""Generic aggregate query capability."""

from typing import Any

from oracle_ebs_chatbot.clients.ords_client import OrdsClient
from oracle_ebs_chatbot.domain.registry import DomainRegistry
from oracle_ebs_chatbot.tools.base import BaseTool, ToolResult


class AggregateQueryTool(BaseTool):
    """Execute a governed metric and dimension query."""

    name = "aggregate_query"
    description = (
        "Calculate a governed metric grouped by approved dimensions "
        "with optional filters."
    )

    def __init__(
        self,
        ords_client: OrdsClient,
        registry: DomainRegistry,
    ) -> None:
        self.ords_client = ords_client
        self.registry = registry

    def validate(self, parameters: dict[str, Any]) -> None:
        """Validate an aggregate query against the domain registry."""

        metric = parameters.get("metric")
        dimensions = parameters.get("dimensions", [])
        filters = parameters.get("filters", {})

        if not isinstance(metric, str) or not metric.strip():
            raise ValueError("metric is required")

        if not isinstance(dimensions, list):
            raise ValueError("dimensions must be a list")

        if not all(isinstance(item, str) for item in dimensions):
            raise ValueError("dimensions must contain only strings")

        if not isinstance(filters, dict):
            raise ValueError("filters must be an object")

        if self.registry.get_metric(metric) is None:
            raise ValueError(f"Unknown metric: {metric}")

        unknown_dimensions = [
            dimension
            for dimension in dimensions
            if self.registry.get_dimension(dimension) is None
        ]

        if unknown_dimensions:
            raise ValueError(f"Unknown dimensions: {', '.join(unknown_dimensions)}")

        if not self.registry.is_combination_approved(
            metric,
            set(dimensions),
        ):
            raise ValueError(
                f"Metric '{metric}' is not approved with the " f"requested dimensions."
            )

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        """Validate and execute the aggregate query."""

        self.validate(parameters)

        metric = str(parameters["metric"])
        dimensions = list(parameters.get("dimensions", []))
        filters = dict(parameters.get("filters", {}))

        try:
            data = self.ords_client.aggregate(
                metric=metric,
                dimensions=dimensions,
                filters=filters,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

        return ToolResult(
            success=True,
            data=data,
        )
