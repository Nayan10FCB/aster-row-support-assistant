from order_tool import OrderTool


def main():

    tool = OrderTool()

    test_ids = [
        "ORD-1001",
        "ord-1001",
        "ORD 1001",
        "ORD_1001",
        "ORD-999999",
        "",
        "hello",
    ]

    for order_id in test_ids:

        print("\n" + "=" * 60)
        print("LOOKUP:", repr(order_id))
        print("=" * 60)

        result = tool.lookup(order_id)

        print(result)


if __name__ == "__main__":
    main()