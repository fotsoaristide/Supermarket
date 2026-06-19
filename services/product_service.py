class ProductService:

    def __init__(self, repository):
        self.repository = repository

    def initialize_database(self):
        self.repository.create_table()

    def add_product(self, product):
     
        if product.purchase_price < 0:
            raise ValueError(
                "The purchase price must be a positive value."
            )

        if product.selling_price < 0:
            raise ValueError(
                "The selling price must be a positive value."
            )

        if product.quantity < 0:
            raise ValueError(
                "The quantity cannot be negative."
            )
        self.repository.add_product(product)

    def get_product_by_barcode(self, barcode: str):
        return self.repository.get_by_barcode(barcode)

    def search_products(self, keyword: str):
        return self.repository.search(keyword)
    
    def update_product(self, product):
        if product.purchase_price < 0:
            raise ValueError("Purchase price must be positive")

        if product.selling_price < 0:
            raise ValueError("Selling price must be positive")

        if product.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.repository.update_product(product)

    def get_all_products(self):
        return self.repository.get_all_products()
