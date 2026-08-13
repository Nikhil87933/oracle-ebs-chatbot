import httpx

from oracle_ebs_chatbot.clients.ords_client import OrdsClient


def test_ords_client_get_entity_boundary() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert str(request.url) == ("http://fake-ords/purchase_order/PO-1001")

        return httpx.Response(
            200,
            json={
                "po_number": "PO-1001",
                "status": "APPROVED",
                "supplier": "ABC Supplies",
                "amount": 125000,
            },
        )

    transport = httpx.MockTransport(handler)

    http_client = httpx.Client(transport=transport)

    client = OrdsClient(
        base_url="http://fake-ords",
        http_client=http_client,
    )

    result = client.get_entity(
        entity="purchase_order",
        identifier="PO-1001",
    )

    assert result == {
        "po_number": "PO-1001",
        "status": "APPROVED",
        "supplier": "ABC Supplies",
        "amount": 125000,
    }

    http_client.close()
