from unittest.mock import Mock

import httpx
import pytest

from oracle_ebs_chatbot.clients.ords_client import OrdsClient


def test_get_entity_sends_correct_request() -> None:
    http_client = Mock(spec=httpx.Client)

    request = httpx.Request(
        "GET",
        "http://ords.example.com/purchase_order/PO-1001",
    )

    response = httpx.Response(
        200,
        request=request,
        json={
            "id": "PO-1001",
            "status": "OPEN",
        },
    )

    http_client.get.return_value = response

    client = OrdsClient(
        base_url="http://ords.example.com/",
        timeout=15.0,
        http_client=http_client,
    )

    result = client.get_entity(
        entity="purchase_order",
        identifier="PO-1001",
    )

    assert result == {
        "id": "PO-1001",
        "status": "OPEN",
    }

    http_client.get.assert_called_once_with(
        "http://ords.example.com/purchase_order/PO-1001",
        headers={},
        timeout=15.0,
    )


def test_get_entity_raises_for_http_error() -> None:
    http_client = Mock(spec=httpx.Client)

    request = httpx.Request(
        "GET",
        "http://ords.example.com/purchase_order/PO-1001",
    )

    response = httpx.Response(
        404,
        request=request,
    )

    http_client.get.return_value = response

    client = OrdsClient(
        base_url="http://ords.example.com",
        http_client=http_client,
    )

    with pytest.raises(httpx.HTTPStatusError):
        client.get_entity(
            entity="purchase_order",
            identifier="PO-1001",
        )


def test_get_entity_rejects_non_object_response() -> None:
    http_client = Mock(spec=httpx.Client)

    request = httpx.Request(
        "GET",
        "http://ords.example.com/purchase_order/PO-1001",
    )

    response = httpx.Response(
        200,
        request=request,
        json=["unexpected", "list"],
    )

    http_client.get.return_value = response

    client = OrdsClient(
        base_url="http://ords.example.com",
        http_client=http_client,
    )

    with pytest.raises(
        ValueError,
        match="ORDS entity response must be an object",
    ):
        client.get_entity(
            entity="purchase_order",
            identifier="PO-1001",
        )


def test_aggregate_sends_correct_request() -> None:
    http_client = Mock(spec=httpx.Client)

    request = httpx.Request(
        "POST",
        "http://ords.example.com/aggregate",
    )

    response = httpx.Response(
        200,
        request=request,
        json=[
            {
                "supplier": "ACME",
                "value": 125000,
            }
        ],
    )

    http_client.post.return_value = response

    client = OrdsClient(
        base_url="http://ords.example.com/",
        timeout=20.0,
        http_client=http_client,
    )

    result = client.aggregate(
        metric="po_amount",
        dimensions=["supplier"],
        filters={"status": "OPEN"},
    )

    assert result == [
        {
            "supplier": "ACME",
            "value": 125000,
        }
    ]

    http_client.post.assert_called_once_with(
        "http://ords.example.com/aggregate",
        headers={},
        json={
            "metric": "po_amount",
            "dimensions": ["supplier"],
            "filters": {"status": "OPEN"},
        },
        timeout=20.0,
    )


def test_aggregate_raises_for_http_error() -> None:
    http_client = Mock(spec=httpx.Client)

    request = httpx.Request(
        "POST",
        "http://ords.example.com/aggregate",
    )

    response = httpx.Response(
        500,
        request=request,
    )

    http_client.post.return_value = response

    client = OrdsClient(
        base_url="http://ords.example.com",
        http_client=http_client,
    )

    with pytest.raises(httpx.HTTPStatusError):
        client.aggregate(
            metric="po_amount",
            dimensions=["supplier"],
            filters={},
        )


def test_aggregate_rejects_non_list_response() -> None:
    http_client = Mock(spec=httpx.Client)

    request = httpx.Request(
        "POST",
        "http://ords.example.com/aggregate",
    )

    response = httpx.Response(
        200,
        request=request,
        json={
            "unexpected": "object",
        },
    )

    http_client.post.return_value = response

    client = OrdsClient(
        base_url="http://ords.example.com",
        http_client=http_client,
    )

    with pytest.raises(
        ValueError,
        match="ORDS aggregate response must be a list",
    ):
        client.aggregate(
            metric="po_amount",
            dimensions=["supplier"],
            filters={},
        )


def test_get_entity_sends_custom_headers() -> None:
    http_client = Mock(spec=httpx.Client)

    request = httpx.Request(
        "GET",
        "http://ords.example.com/purchase_order/PO-1001",
    )

    response = httpx.Response(
        200,
        request=request,
        json={"id": "PO-1001"},
    )

    http_client.get.return_value = response

    client = OrdsClient(
        base_url="http://ords.example.com",
        headers={
            "Authorization": "Bearer test-token",
            "X-User": "nikhil",
        },
        http_client=http_client,
    )

    client.get_entity(
        entity="purchase_order",
        identifier="PO-1001",
    )

    http_client.get.assert_called_once_with(
        "http://ords.example.com/purchase_order/PO-1001",
        headers={
            "Authorization": "Bearer test-token",
            "X-User": "nikhil",
        },
        timeout=10.0,
    )


def test_aggregate_sends_custom_headers() -> None:
    http_client = Mock(spec=httpx.Client)

    request = httpx.Request(
        "POST",
        "http://ords.example.com/aggregate",
    )

    response = httpx.Response(
        200,
        request=request,
        json=[],
    )

    http_client.post.return_value = response

    client = OrdsClient(
        base_url="http://ords.example.com",
        headers={
            "Authorization": "Bearer test-token",
        },
        http_client=http_client,
    )

    client.aggregate(
        metric="po_amount",
        dimensions=[],
        filters={},
    )

    http_client.post.assert_called_once_with(
        "http://ords.example.com/aggregate",
        headers={
            "Authorization": "Bearer test-token",
        },
        json={
            "metric": "po_amount",
            "dimensions": [],
            "filters": {},
        },
        timeout=10.0,
    )
