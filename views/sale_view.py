class SaleView:
    """
    CLI interface for sales.
    Handles input/output only.
    """

    # =========================
    # INPUTS
    # =========================
    def get_product_id(self):
        return int(input("Scanner produit (ID): "))

    def get_quantity(self):
        return int(input("Quantité: "))

    # =========================
    # MESSAGES
    # =========================
    def show_message(self, message):
        print(f"[INFO] {message}")

    def show_error(self, message):
        print(f"[ERREUR] {message}")

    # =========================
    # DISPLAY SALE
    # =========================
    def display_sale(self, sale_data):
        sale = sale_data["sale"]
        items = sale_data["items"]

        print("\n" + "=" * 40)
        print(f"VENTE ID: {sale['id']}")
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
        print("1. Ajouter produit")
        print("2. Voir panier")
        print("3. Terminer vente")
        print("4. Annuler")