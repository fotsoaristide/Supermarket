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

        print("\n" + "=" * 40)
        print(f"SALE ID: {sale['id']}")
        print(f"DATE: {sale['created_at']}")
        print("-" * 40)

        for item in items:
            print(
                f"{item['product_name']} x{item['quantity']} "
                f"= {item['subtotal']} FCFA"
            )

        print("-" * 40)
        print(f"TOTAL: {sale['total']} FCFA")
        print("=" * 40 + "\n")

    # =========================
    # MENU SALE (optionnel mais utile)
    # =========================
    def show_sale_menu(self):
        print("\n===== CAISSE =====")
        print("1. Add product")
        print("2. View cart")
        print("3. End sale")
        print("4. Cancel")