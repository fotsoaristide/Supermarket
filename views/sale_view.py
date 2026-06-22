from datetime import datetime
from utils.formatter import Formatter


class SaleView:
    """
    CLI interface for sales.
    Handles input/output only.
    """

    # =========================
    # INPUTS
    # =========================
    def get_product_id(self):
        return int(input("Product scanner (ID): "))

    def get_quantity(self):
        return int(input("Quantity: "))

    # =========================
    # MESSAGES
    # =========================
    def show_message(self, message):
        print(f"[INFO] {message}")

    def show_error(self, message):
        print(f"[ERROR] {message}")

    # =========================
    # DISPLAY SALE
    # =========================
    def display_sale(self, sale_data):
        sale = sale_data["sale"]
        items = sale_data["items"]

        print("\n" + "=" * 50)
        print(f"Sale ID: {sale['id']}")
        print(f"DATE: {Formatter.format_date(sale['created_at'])}")
        print("-" * 50)

        for item in items:
            name = item["product_name"]
            qty = item["quantity"]
            unit = item["unit_price"]
            subtotal = item["subtotal"]
            # Nom multi-ligne
            name_lines = Formatter.wrap_text(name, 25)

            for line in name_lines:
                print(line)

            left = f"{qty} x {unit:.0f}"
            right = Formatter.format_money(subtotal)

            print(left.ljust(25) + right)
            print()

        print("-" * 50)
        print(
            "TOTAL".ljust(25) +
            Formatter.format_money(sale["total"])
        )
        print("=" * 50 + "\n")

    # =========================
    # MENU SALE (optionnel mais utile)
    # =========================
    def show_sale_menu(self):
        print("\n===== SALE MENU =====")
        print("1. Add product")
        print("2. View cart")
        print("3. Update quantity")
        print("4. Remove product")
        print("5. Cancel sale")
        print("6. Complete sale")
    
    def get_update_product_id(self):
        """
        Ask the user for the product ID to update.
        """
        return int(input("Product ID: "))
    
    def get_new_quantity(self):
        """
        Ask the user for the new quantity.
        """
        return int(input("New quantity: "))
    
    def display_sales_history(self, sales):

        print("\n===== SALES HISTORY =====")
        print(f"{'ID':<5}{'DATE':<18}{'TOTAL':>12}")
        print("-" * 45)

        for s in sales:

            raw_date = s["created_at"]
            raw_total = s["total"]

            formatted_date = Formatter.format_date(raw_date)
            formatted_total = Formatter.format_money(raw_total)

            print(
                f"{s['id']:<5}"
                f"{formatted_date:<18}"
                f"{formatted_total:>12}"
            )

        print("-" * 45)
