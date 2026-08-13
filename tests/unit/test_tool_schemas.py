from oracle_ebs_chatbot.domain.default_registry import create_default_registry
from oracle_ebs_chatbot.llm.tool_schemas import get_tool_schemas


def test_tool_schemas_expose_only_controlled_tools() -> None:
    schemas = get_tool_schemas(create_default_registry())

    names = {schema["function"]["name"] for schema in schemas}

    assert names == {
        "entity_lookup",
        "aggregate_query",
    }


def test_entity_lookup_schema_contains_required_parameters() -> None:
    schemas = get_tool_schemas(create_default_registry())

    entity_schema = next(
        schema for schema in schemas if schema["function"]["name"] == "entity_lookup"
    )

    properties = entity_schema["function"]["parameters"]["properties"]

    assert "entity" in properties
    assert "identifier" in properties
    assert "purchase_order" in properties["entity"]["enum"]


def test_aggregate_query_schema_contains_query_parameters() -> None:
    schemas = get_tool_schemas(create_default_registry())

    aggregate_schema = next(
        schema for schema in schemas if schema["function"]["name"] == "aggregate_query"
    )

    properties = aggregate_schema["function"]["parameters"]["properties"]

    assert "metric" in properties
    assert "dimensions" in properties
    assert "filters" in properties

    assert "po_amount" in properties["metric"]["enum"]
    assert "po_count" in properties["metric"]["enum"]
