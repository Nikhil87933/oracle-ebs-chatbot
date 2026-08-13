"""Governed domain metadata registry."""

from pydantic import BaseModel, Field, model_validator


class Entity(BaseModel):
    """A business entity that the chatbot can understand."""

    name: str
    description: str


class Metric(BaseModel):
    """A governed business metric."""

    name: str
    description: str
    entity: str


class Dimension(BaseModel):
    """A governed dimension used to group or filter metrics."""

    name: str
    description: str
    entity: str


class ApprovedCombination(BaseModel):
    """A governed metric and dimension combination."""

    metric: str
    dimensions: frozenset[str] = frozenset()


class DomainRegistry(BaseModel):
    """Collection of governed domain metadata."""

    entities: dict[str, Entity] = Field(default_factory=dict)
    metrics: dict[str, Metric] = Field(default_factory=dict)
    dimensions: dict[str, Dimension] = Field(default_factory=dict)
    approved_combinations: list[ApprovedCombination] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_references(self) -> "DomainRegistry":
        """Ensure all metadata references known registry entries."""

        for metric in self.metrics.values():
            if metric.entity not in self.entities:
                raise ValueError(
                    f"Metric '{metric.name}' references unknown "
                    f"entity '{metric.entity}'."
                )

        for dimension in self.dimensions.values():
            if dimension.entity not in self.entities:
                raise ValueError(
                    f"Dimension '{dimension.name}' references unknown "
                    f"entity '{dimension.entity}'."
                )

        for combination in self.approved_combinations:
            if combination.metric not in self.metrics:
                raise ValueError(
                    f"Approved combination references unknown "
                    f"metric '{combination.metric}'."
                )

            for dimension_name in combination.dimensions:
                if dimension_name not in self.dimensions:
                    raise ValueError(
                        f"Approved combination references unknown "
                        f"dimension '{dimension_name}'."
                    )

        return self

    def get_entity(self, name: str) -> Entity | None:
        """Return an entity by name."""
        return self.entities.get(name)

    def get_metric(self, name: str) -> Metric | None:
        """Return a metric by name."""
        return self.metrics.get(name)

    def get_dimension(self, name: str) -> Dimension | None:
        """Return a dimension by name."""
        return self.dimensions.get(name)

    def is_combination_approved(
        self,
        metric: str,
        dimensions: set[str],
    ) -> bool:
        """Return whether a metric/dimension combination is approved."""
        requested_dimensions = frozenset(dimensions)

        return any(
            combination.metric == metric
            and combination.dimensions == requested_dimensions
            for combination in self.approved_combinations
        )
