class SaleController:
    """
    Handles user interactions for sales (CLI layer).
    """

    def __init__(
        self,
        sale_service,
        product_service,
        sale_view
    ):
        self.sale_service = sale_service
        self.product_service = product_service
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

    def display_report(
        self,
        title,
        period,
        sales_count,
        revenue,
        profit=None
    ):
        print("\n========================================")
        print(f"{title}")
        print("========================================")
        print(f"Period          : {period}")
        print(f"Number of sales : {sales_count}")
        print(f"Revenue         : {revenue} FCFA")

        if profit is not None:
            print(f"Cost/Profit info included")

            print(f"Profit          : {profit} FCFA")

        print("========================================")

    def show_daily_report(self):
        """
        Display daily accounting report.
        """

        report = self.sale_service.get_daily_report()

        self.display_report(
            report["title"],
            report["period"],
            report["sales_count"],
            report["revenue"]
        )

    def show_weekly_report(self):
        """
        Display weekly accounting report.
        """
        report = self.sale_service.get_weekly_report()

        self.display_report(
            report["title"],
            report["period"],
            report["sales_count"],
            report["revenue"]
        )
    def show_monthly_report(self):
        """
        Display monthly accounting report.
        """

        report = self.sale_service.get_monthly_report()

        self.display_report(
            report["title"],
            report["period"],
            report["sales_count"],
            report["revenue"]
        )

    def show_profit_report(self):
        """
        Display profit report.
        """

        report = self.sale_service.get_profit_report()

        self.display_report(
            report["title"],
            report["period"],
            report["sales_count"],
            report["revenue"],
            report["profit"]
        )
    
    def show_stock_valuation(self):
        """
        Display stock valuation report.
        """

        report = self.sale_service.get_stock_valuation()

        print("\n========================================")
        print(f"{report['title']}")
        print("========================================")

        print(f"Products count : {report['products_count']}")
        print(f"Total stock value : {report['total_value']} FCFA")

        print("========================================")
    
    def show_stock_valuation_details(self):
        """
         detailed stock valuation.
        """

        report = self.sale_service.get_stock_valuation_details()

        print("\n========================================")
        print(f"{report['title']}")
        print("========================================")

        for item in report["items"]:
            print(
                f"{item['name']} | "
                f"Qty: {item['quantity']} | "
                f"Unit: {item['unit_cost']} | "
                f"Value: {item['value']}"
            )

        print("========================================")
        print(f"TOTAL STOCK VALUE: {report['total_value']} FCFA")

    def show_low_stock_report(self):
        """
        Display products with low stock.
        """

        products = self.product_service.get_low_stock_products()

        print("\n========================================")
        print("          LOW STOCK REPORT")
        print("========================================")

        if not products:
            print("No product requires restocking.")
        else:

            print(
                f"{'ID':<5}"
                f"{'PRODUCT':<28}"
                f"{'STOCK':>8}"
                f"{'MIN':>8}"
            )

            print("-" * 50)

            for product in products:
                print(
                    f"{product.id:<5}"
                    f"{product.name[:27]:<28}"
                    f"{product.quantity:>8}"
                    f"{product.minimum_stock:>8}"
                )

        print("========================================")
    
    def show_top_selling_products(self):
        report = self.sale_service.get_top_selling_report()

        print("\n========================================")
        print(f"{report['title']}")
        print("========================================")

        if not report["items"]:
            print("No sales data available.")
            return

        print(f"{'ID':<5}{'PRODUCT':<25}{'QTY SOLD':<10}{'REVENUE'}")
        print("-" * 60)

        for item in report["items"]:
            print(
                f"{item['id']:<5}"
                f"{item['name'][:24]:<25}"
                f"{item['quantity_sold']:<10}"
                f"{item['revenue']} FCFA"
            )

        print("========================================")

    def show_unsold_products(self):
        report = self.sale_service.get_unsold_report()

        print("\n========================================")
        print(f"{report['title']}")
        print("========================================")

        if not report["items"]:
            print("All products have been sold.")
            return

        print(f"{'ID':<5}{'PRODUCT':<30}{'STOCK'}")
        print("-" * 50)

        for product in report["items"]:
            print(
                f"{product.id:<5}"
                f"{product.name[:29]:<30}"
                f"{product.quantity}"
            )

        print("========================================")

    def accounting_menu(self):
        while True:
            print("\n===== ACCOUNTING =====")
            print("1. Daily report")
            print("2. Weekly report")
            print("3. Monthly report")
            print("4. Profit report")
            print("5. Stock valuation")
            print("6. Low stock report")
            print("7. Top Selling Products")
            print("8. Unsold Products")
            print("9. Back")

            choice = input("Choice: ")

            if choice == "1":
                self.show_daily_report()

            elif choice == "2":
                self.show_weekly_report()

            elif choice == "3":
                self.show_monthly_report()
            
            elif choice == "4":
                self.show_profit_report()

            elif choice == "5":
                self.show_stock_valuation()

            elif choice == "6":
                self.show_low_stock_report()

            elif choice == "7":
                self.show_top_selling_products()

            elif choice == "8":
                self.show_unsold_products()

            elif choice == "9":
                break
   