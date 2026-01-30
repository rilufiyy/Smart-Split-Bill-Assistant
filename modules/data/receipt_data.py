from dataclasses import dataclass, field, asdict
from typing import Dict

import pandas as pd

from .base import IDGenerator


class ItemIDGenerator(IDGenerator):
    """Generator for item ID in the receipt."""
    pass


@dataclass
class ItemData:
    """Item data from the receipt."""

    name: str
    count: int
    total_price: float
    id: int = field(default_factory=ItemIDGenerator.get)

    @property
    def unit_price(self) -> float:
        """Unit price of item (safe from zero division)."""
        if self.count <= 0:
            return self.total_price
        return self.total_price / self.count


@dataclass
class ReceiptData:
    """Receipt data from AI reading."""

    items: Dict[int, ItemData]
    total: float

    @property
    def subtotal(self) -> float:
        """Sum of all item total prices."""
        return sum(item.total_price for item in self.items.values())

    def to_items_df(self) -> pd.DataFrame:
        """Convert items to pandas DataFrame."""
        if not self.items:
            return pd.DataFrame(
                columns=["id", "name", "count", "total_price"]
            )

        data = []
        for item in self.items.values():
            data.append({
                "id": item.id,
                "name": item.name,
                "count": item.count,
                "total_price": item.total_price,
            })

        return pd.DataFrame(data)

    @classmethod
    def from_items_df(cls, items_df: pd.DataFrame, total: float) -> "ReceiptData":
        """
        Build ReceiptData from DataFrame.
        Expected columns: name, count, total_price
        """

        items: Dict[int, ItemData] = {}

        if items_df is None or items_df.empty:
            return cls(items={}, total=total)

        for _, row in items_df.iterrows():
            # ---- SAFE PARSING ----
            name = str(row.get("name", "")).strip()
            if not name:
                continue

            try:
                count = int(row.get("count", 1))
            except (TypeError, ValueError):
                count = 1
            count = max(count, 1)

            try:
                total_price = float(row.get("total_price", 0.0))
            except (TypeError, ValueError):
                total_price = 0.0

            item = ItemData(
                name=name,
                count=count,
                total_price=total_price,
            )

            items[item.id] = item

        return cls(items=items, total=total)