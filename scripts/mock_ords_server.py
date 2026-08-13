"""Local mock ORDS server for the chatbot POC."""

from fastapi import FastAPI

app = FastAPI(title="Mock ORDS")

PURCHASE_ORDERS = {
    "PO-1001": {
        "po_number": "PO-1001",
        "status": "APPROVED",
        "supplier": "ABC Supplies",
        "amount": 125000,
    },
    "PO-1002": {
        "po_number": "PO-1002",
        "status": "OPEN",
        "supplier": "XYZ Industries",
        "amount": 87500,
    },
}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/purchase_order/{identifier}")
def get_purchase_order(identifier: str) -> dict:
    purchase_order = PURCHASE_ORDERS.get(identifier)

    if purchase_order is None:
        return {
            "error": "Purchase order not found",
            "identifier": identifier,
        }

    return purchase_order


@app.post("/aggregate")
def aggregate(payload: dict) -> list[dict]:
    metric = payload.get("metric")
    dimensions = payload.get("dimensions", [])
    filters = payload.get("filters", {})

    rows = list(PURCHASE_ORDERS.values())

    status = filters.get("status")
    if status:
        rows = [row for row in rows if row["status"] == status]

    if metric == "po_count":
        return [{"count": len(rows)}]

    if metric == "po_amount":
        if dimensions == ["supplier"]:
            return [
                {
                    "supplier": row["supplier"],
                    "value": row["amount"],
                }
                for row in rows
            ]

        return [{"value": sum(row["amount"] for row in rows)}]

    return [{"error": f"Unsupported metric: {metric}"}]
