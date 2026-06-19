from dataclasses import dataclass, field
from datetime import datetime

from models.sale_item import SaleItem


@dataclass(slots=True)
class Sale:
    """
    Represents a customer sale.
    """

    id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)
    items: list[SaleItem] = field(default_factory=list)

    @property
    def total(self) -> float:
        """
        Calculate the total amount of the sale.
        """
        return sum(item.subtotal for item in self.items)

    @property
    def total_items(self) -> int:
        """
        Return the total quantity of items sold.
        """
        return sum(item.quantity for item in self.items)