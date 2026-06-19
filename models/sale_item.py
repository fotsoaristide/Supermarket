from dataclasses import dataclass


@dataclass(slots=True)
class SaleItem:
    """
    Represents a single line in a sale.
    """

    product_id: int
    product_name: str
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        """
        Calculate the subtotal of this sale line.
        """
        return self.quantity * self.unit_price