class ProductService:

    def __init__(self, repository):
        self.repository = repository

    def initialize_database(self):
        self.repository.create_table()

    def add_product(self, product):
     
        if product.purchase_price < 0:
            raise ValueError(
                "Le prix d'achat doit être positif."
            )

        if product.selling_price < 0:
            raise ValueError(
                "Le prix de vente doit être positif."
            )

        if product.quantity < 0:
            raise ValueError(
                "La quantité ne peut pas être négative."
            )
        self.repository.add_product(product)

    def get_all_products(self):
        return self.repository.get_all_products()