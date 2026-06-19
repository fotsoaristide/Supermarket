class MenuController:

    def __init__(self, menu_view, product_controller, sale_controller):
        self.menu_view = menu_view
        self.product_controller = product_controller
        self.sale_controller = sale_controller

    def run(self):
        while True:

            self.menu_view.display_menu()

            choice = self.menu_view.get_choice()

            if choice == "1":
                self.product_controller.add_product()

            elif choice == "2":
                self.product_controller.display_products()

            elif choice == "3":
                self.product_controller.search_product()

            elif choice == "4":
                self.product_controller.update_product()

            elif choice == "5":
                self.product_controller.delete_product()

            elif choice == "6":
                self.handle_sale()

            elif choice == "7":
                break

            else:
                self.menu_view.show_error("Invalid choice")

    # =========================
    # SALES FLOW
    # =========================
    def handle_sale(self):
        self.sale_controller.start_sale()

        while True:
            print("\n1. Add product")
            print("2. View cart")
            print("3. End sale")

            choice = input("Choice: ")

            if choice == "1":
                self.sale_controller.add_product()

            elif choice == "2":
                self.sale_controller.show_current_sale()

            elif choice == "3":
                self.sale_controller.end_sale()
                break

            else:
                print("Invalid choice")
