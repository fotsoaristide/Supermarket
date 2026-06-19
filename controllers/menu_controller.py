class MenuController:

    def __init__(self, view, product_controller):
        self.view = view
        self.product_controller = product_controller

    def run(self):

        self.product_controller.initialize()

        while True:

            choice = self.view.show_menu()

            if choice == "1":
                self.product_controller.add_product()

            elif choice == "2":
                self.product_controller.display_products()

            elif choice == "6":
                self.view.goodbye()
                break

            else:
                self.view.invalid_choice()
