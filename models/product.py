from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Product:
    id: int | None = None

    barcode: str = ""
    name: str = ""
    category: str = ""

    purchase_price: float = 0.0
    selling_price: float = 0.0

    quantity: int = 0
    minimum_stock: int = 5

    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    @property
    def profit(self) -> float:
        return self.selling_price - self.purchase_price

    @property
    def is_low_stock(self) -> bool:
        return self.quantity <= self.minimum_stock
