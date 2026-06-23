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
            self.sale_view.show_message(
                f"Added: ID {product_id} x{quantity}"
            )
            self.show_current_sale()
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

    def remove_product(self):
        """
        Remove product from current sale.
        """

        product_id = self.sale_view.get_update_product_id()

        try:
            self.sale_service.remove_item(product_id)

            self.sale_view.show_message("Product removed successfully.")

            self.show_current_sale()

        except Exception as e:
            self.sale_view.show_error(str(e))

    def cancel_sale(self):
        """
        Cancel current sale.
        """

        try:
            self.sale_service.cancel_sale()

            self.sale_view.show_message("Sale cancelled successfully.")

        except Exception as e:
            self.sale_view.show_error(str(e))

    # =========================
    # END SALE
    # =========================
    def end_sale(self):
        try:
            total = self.sale_service.end_sale()
            if total is None:
                self.sale_view.show_error("No active sale to end.")
                return

            self.sale_view.show_message(
                f"Sale completed. TOTAL = {total} FCFA"
            )

            # =========================
            # RECEIPT MENU (MODE PRO)
            # =========================
            while True:
                print("\n===== RECEIPT OPTIONS =====")
                print("1. Print ticket")
                print("2. Do not print")
                print("3. Reprint last ticket")

                choice = input("Choice: ")

                if choice == "1":
                    self.sale_service.generate_last_ticket()
                    self.sale_service.print_last_ticket()
                    break

                elif choice == "2":
                    break

                elif choice == "3":
                    print("\n" + self.sale_service.reprint_last_ticket())

                else:
                    print("Invalid choice")

        except Exception as e:
            self.sale_view.show_error(str(e))

    def update_item_quantity(self):
        """
        Update the quantity of a product in the current sale.
        """

        product_id = self.sale_view.get_update_product_id()
        new_quantity = self.sale_view.get_new_quantity()
        try:
            self.sale_service.update_item_quantity(
                product_id,
                new_quantity
            )

            self.sale_view.show_message(
                "Quantity updated successfully."
            )

            self.show_current_sale()

        except Exception as e:
            self.sale_view.show_error(str(e))

    def show_sales_history(self):
        """
        Display sales history and allow the user to view a sale.
        """
        try:
            sales = self.sale_service.get_sales_history()

            if not sales:
                self.sale_view.show_message("No sales found.")
                return

            self.sale_view.display_sales_history(sales)

            sale_id = int(input("Enter sale ID to view: "))

            data = self.sale_service.get_sale_details(sale_id)

            self.sale_view.display_sale(data)

            print("\n1. Print ticket")
            print("2. Back")

            choice = input("Choice: ")

            if choice == "1":
                ticket = self.sale_service.ticket_printer.generate(
                    data["sale"],
                    data["items"]
                )
                self.sale_service.last_ticket = ticket
                self.sale_service.thermal_printer.print_receipt(ticket)

        except Exception as e:
            self.sale_view.show_error(str(e))
