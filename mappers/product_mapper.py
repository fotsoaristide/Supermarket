from models.product import Product


class ProductMapper:

    @staticmethod
    def from_row(row):

        return Product(
            id=row["id"],
            barcode=row["barcode"],
            name=row["name"],
            category=row["category"],
            purchase_price=row["purchase_price"],
            selling_price=row["selling_price"],
            quantity=row["quantity"],
            minimum_stock=row["minimum_stock"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    
    @staticmethod
    def to_row(product):

        return (
            product.id,
            product.barcode,
            product.name,
            product.category,
            product.purchase_price,
            product.selling_price,
            product.quantity,
            product.minimum_stock,
            product.created_at,
            product.updated_at
        )
    
    @staticmethod
    def to_dict(product):

        return {
            "id": product.id,
            "barcode": product.barcode,
            "name": product.name,
            "category": product.category,
            "purchase_price": product.purchase_price,
            "selling_price": product.selling_price,
            "quantity": product.quantity,
            "minimum_stock": product.minimum_stock,
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }
