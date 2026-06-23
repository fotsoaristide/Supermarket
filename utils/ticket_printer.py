from config.store_config import StoreConfig
from utils.formatter import Formatter


class TicketPrinter:

    def __init__(self):
        self.width = StoreConfig.RECEIPT_WIDTH

    # =========================
    # CENTER TEXT
    # =========================
    def center(self, text):
        return text.center(self.width)

    # =========================
    # LINE
    # =========================
    def line(self):
        return "-" * self.width
    
    # =========================
    # FORMAT ITEM LINE
    # =========================
    def format_item(self, name, qty, price, subtotal):
        """
        Format one receipt item.
        """
        lines = []

        # Nom découpé automatiquement
        lines.extend(
            Formatter.wrap_text(name, self.width - 6)
        )

        left = f"{qty} x {price:.0f}"

        right = f"{subtotal:,.0f}".replace(",", " ")

        lines.append(
            left.ljust(self.width - len(right))
            + right
        )
        return "\n".join(lines)
    
    # =========================
    # GENERATE TICKET
    # =========================
    def generate(self, sale, items):
        """
        Generate the complete receipt.
        """
        lines = []

        lines.extend(self.build_header())

        lines.extend(
            self.build_sale_info(sale)
        )

        lines.extend(
            self.build_items(items)
        )

        lines.extend(
            self.build_total(sale)
        )

        lines.extend(
            self.build_footer()
        )
        return "\n".join(lines)
    
    def build_header(self):
        """
        Build receipt header.
        """
        lines = []

        lines.append("=" * self.width)
        lines.append(self.center(StoreConfig.STORE_NAME))
        lines.append(self.center(StoreConfig.STORE_SLOGAN))
        lines.append(self.center(StoreConfig.STORE_ADDRESS))

        if StoreConfig.STORE_PHONE:
            lines.append(self.center(StoreConfig.STORE_PHONE))
        lines.append("=" * self.width)
        return lines
    
    def build_sale_info(self, sale):
        """
        Build sale information section.
        """
        lines = []

        lines.append(f"Ticket : #{sale['id']:06d}")
        lines.append(
            f"Date   : {Formatter.format_date(sale['created_at'])}"
        )
        lines.append(self.line())
        return lines
    
    def build_items(self, items):
        """
        Build receipt items.
        """
        lines = []

        for item in items:
            lines.append(
                self.format_item(
                    item["product_name"],
                    item["quantity"],
                    item["unit_price"],
                    item["subtotal"]
                )
            )
            lines.append("")
        lines.append(self.line())
        return lines
    
    def build_total(self, sale):
        """
        Build the total section.
        """
        lines = []

        total = Formatter.format_money(sale["total"])

        lines.append(
            "TOTAL À PAYER".ljust(14) +
            total.rjust(self.width - 14)
        )
        lines.append(self.line())
        return lines
    
    def build_footer(self):
        """
        Build receipt footer.
        """
        lines = []

        lines.append(self.center(StoreConfig.FOOTER_MESSAGE))
        return lines
