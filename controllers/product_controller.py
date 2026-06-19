"""Product Controller for handling product-related operations."""

from models.product import Product

class ProductController:

    def __init__(self, service, view):
        self.service = service
        self.view = view

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
