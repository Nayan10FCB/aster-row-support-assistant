import json
import re
from pathlib import Path


ORDERS_FILE = Path("data/orders.json")


class OrderTool:

    def __init__(self):
        self.orders = self._load_orders()

    def _load_orders(self):
        """Load the supplied order dataset."""

        with ORDERS_FILE.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        # Support either a list of orders or
        # {"orders": [...]}
        if isinstance(data, dict):
            return data.get("orders", [])

        return data

    def _normalize_order_id(self, order_id):
        """Normalize common order-ID formatting."""

        if not order_id:
            return None

        order_id = str(order_id).strip().upper()

        # Remove spaces and common punctuation.
        order_id = re.sub(
            r"[\s_-]+",
            "",
            order_id
        )

        # Accept IDs such as:
        # ORD-1001
        # ord 1001
        # ORD_1001
        match = re.match(
            r"^(ORD)(\d+)$",
            order_id
        )

        if not match:
            return None

        return f"{match.group(1)}-{match.group(2)}"

    def lookup(self, order_id):
        """Look up one order safely."""

        normalized_id = self._normalize_order_id(
            order_id
        )

        if not normalized_id:
            return {
                "success": False,
                "error": "Please provide a valid order ID."
            }

        for order in self.orders:

            raw_id = (
                order.get("order_id")
                or order.get("id")
            )

            if not raw_id:
                continue

            stored_id = self._normalize_order_id(
                raw_id
            )

            if stored_id == normalized_id:

                return {
                    "success": True,
                    "order": self._safe_order_data(
                        order
                    )
                }

        return {
            "success": False,
            "error": (
                f"No order was found for "
                f"{normalized_id}."
            )
        }

    def _safe_order_data(self, order):
        """
        Return only customer-safe order fields.

        Never expose internal/private fields.
        """

        allowed_fields = [
            "order_id",
            "status",
            "items",
            "total",
            "currency",
            "order_date",
            "estimated_delivery",
            "tracking_number",
            "shipping_method",
        ]

        safe_data = {}

        for field in allowed_fields:

            if field in order:
                safe_data[field] = order[field]

        return safe_data