"""Tool schemas exposed to the LLM."""

from typing import Any

from oracle_ebs_chatbot.domain.registry import DomainRegistry


def get_tool_schemas(
    registry: DomainRegistry,
) -> list[dict[str, Any]]:
    """Return controlled tool definitions derived from domain metadata."""

    entity_names = sorted(registry.entities)
    metric_names = sorted(registry.metrics)
    dimension_names = sorted(registry.dimensions)

    return [
        {
            "type": "function",
            "function": {
                "name": "entity_lookup",
                "description": (
                    "Fetch a single approved business entity by its identifier."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity": {
                            "type": "string",
                            "enum": entity_names,
                            "description": ("Approved business entity to retrieve."),
                        },
                        "identifier": {
                            "type": "string",
                            "description": "Identifier of the entity.",
                        },
                    },
                    "required": ["entity", "identifier"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "aggregate_query",
                "description": (
                    "Calculate a governed metric grouped by approved "
                    "dimensions with optional filters."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "metric": {
                            "type": "string",
                            "enum": metric_names,
                            "description": "Governed business metric.",
                        },
                        "dimensions": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": dimension_names,
                            },
                            "description": "Approved grouping dimensions.",
                        },
                        "filters": {
                            "type": "object",
                            "additionalProperties": True,
                            "description": "Optional query filters.",
                        },
                    },
                    "required": ["metric"],
                },
            },
        },
    ]
