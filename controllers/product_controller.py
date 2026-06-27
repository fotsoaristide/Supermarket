"""Product Controller for handling product-related operations."""

from models.product import Product

class ProductController:

    def __init__(self, service, view, event_bus):
        self.service = service
        self.view = view
        self.event_bus = event_bus

    def initialize(self):
        self.service.initialize_database()

    def add_product(self):

        (
            barcode,
            name,
            category,
            purchase_price,
            selling_price,
            quantity,
            minimum_stock
        ) = self.view.get_product_information()

        product = Product(
            barcode=barcode,
            name=name,
            category=category,
            purchase_price=purchase_price,
            selling_price=selling_price,
            quantity=quantity,
            minimum_stock=minimum_stock
        )
        try:
            self.service.add_product(product)
            self.view.success_message()
        except ValueError as error:
            self.view.error_message(str(error))

    def display_products(self):

        products = self.service.get_all_products()

        self.view.display_products(products)

    def search_product(self):
        keyword = input("Enter keyword (name/barcode/category): ")

        results = self.service.search_products(keyword)

        if not results:
            self.view.show_error("No product found.")
            return

        self.view.display_products(results)

    def search_by_barcode(self):
        barcode = input("Scan / Enter barcode: ")

        product = self.service.get_product_by_barcode(barcode)

        if not product:
            self.view.show_error("Product not found.")
            return

        self.view.display_products([product])

    def scan_mode(self):
        print("\n=== SCAN MODE (type 'exit' to stop) ===")

        while True:
            barcode = input("Scan barcode: ")

            if barcode.lower() == "exit":
                break
            product = self.service.get_product_by_barcode(barcode)

            if not product:
                self.view.show_error("Product not found.")
                continue

            print(
                f"{product.name} | "
                f"{product.selling_price} FCFA | "
                f"Stock: {product.quantity}"
            )

    def delete_product(self):

        product_id = self.view.get_delete_product_id()

        try:
            self.service.delete_product(product_id)
            print("\nProduct deleted successfully.")
        except ValueError as error:
            self.view.error_message(str(error))
            
    def update_product(self):

        (
            product_id,
            barcode,
            name,
            category,
            purchase_price,
            selling_price,
            quantity,
            minimum_stock
        ) = self.view.get_update_product_info()

        product = Product(
            id=product_id,
            barcode=barcode,
            name=name,
            category=category,
            purchase_price=purchase_price,
            selling_price=selling_price,
            quantity=quantity,
            minimum_stock=minimum_stock
        )

        try:
            self.service.update_product(product)
            self.view.success_message()
        except ValueError as error:
            self.view.error_message(str(error))

    # =========================
    # GUI API
    # =========================

    def add_product_from_model(self, product):
        """
        Add a Product model coming from the GUI.
        """
        self.service.add_product(product)
        self.event_bus.emit("product_changed")

    def update_product_from_model(self, product):
        """
        Update a Product model coming from the GUI.
        """
        self.service.update_product(product)
        self.event_bus.emit("product_changed")

    def delete_product_by_id(self, product_id):
        """
        Delete a product by id (GUI entry point).
        """
        self.service.delete_product(product_id)
        self.event_bus.emit("product_changed")

    # =========================
    # GUI API (CLEAN LAYER)
    # =========================

    def get_all_products(self):
        return self.service.get_all_products()


    def search_products(self, keyword: str):
        return self.service.search_products(keyword)
