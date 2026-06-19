class SaleController:
    """
    Handles user interactions for sales (CLI layer).
    """

    def __init__(self, sale_service, sale_view):
        self.sale_service = sale_service
        self.sale_view = sale_view

    # =========================
    # START SALE
    # =========================
    def start_sale(self):
        sale_id = self.sale_service.start_sale()
        self.sale_view.show_message(f"Sale started (ID: {sale_id})")
        return sale_id

    # =========================
    # ADD PRODUCT FLOW
    # =========================
    def add_product(self):
        product_id = self.sale_view.get_product_id()
        quantity = self.sale_view.get_quantity()

        try:
            self.sale_service.add_product(product_id, quantity)
            self.sale_view.show_message("Product added successfully.")
        except Exception as e:
            self.sale_view.show_error(str(e))

    # =========================
    # SHOW CURRENT SALE
    # =========================
    def show_current_sale(self):
        sale_data = self.sale_service.get_current_sale()

        if not sale_data:
            self.sale_view.show_message("No sale in progress.")
            return

        self.sale_view.display_sale(sale_data)

    # =========================
    # END SALE
    # =========================
    def end_sale(self):
        total = self.sale_service.end_sale()
        self.sale_view.show_message(f"Sale completed. TOTAL = {total} FCFA")
