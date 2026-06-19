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
        print(f"DATE: {sale['created_at']}")
        print("-" * 50)

        for item in items:
            name = item["product_name"]
            qty = item["quantity"]
            unit = item["unit_price"]
            subtotal = item["subtotal"]
            print(f"{name:<15} x{qty:<3} {unit:>6} FCFA  => {subtotal:>6} FCFA")

        print("-" * 50)
        print(f"{'TOTAL':<25} {sale['total']} FCFA")
        print("=" * 50 + "\n")

    # =========================
    # MENU SALE (optionnel mais utile)
    # =========================
    def show_sale_menu(self):
        print("\n===== CAISSE =====")
        print("1. Add product")
        print("2. View cart")
        print("3. End sale")
        print("4. Cancel")