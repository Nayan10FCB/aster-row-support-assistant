from app.order_tool import OrderTool


def test_order_lookup_valid_formats():

    tool = OrderTool()

    test_ids = [
        "ORD-1001",
        "ord-1001",
        "ORD 1001",
        "ORD_1001",
    ]

    for order_id in test_ids:

        result = tool.lookup(order_id)

        assert result["success"] is True
        assert result["order"]["order_id"] == "ORD-1001"
        assert result["order"]["status"] == "pending"


def test_order_lookup_missing_order():

    tool = OrderTool()

    result = tool.lookup("ORD-999999")

    assert result["success"] is False
    assert "No order was found" in result["error"]


def test_order_lookup_invalid_input():

    tool = OrderTool()

    for order_id in ["", "hello"]:

        result = tool.lookup(order_id)

        assert result["success"] is False
        assert "valid order ID" in result["error"]