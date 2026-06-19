"""inventory management repository module"""
from datetime import datetime
from mappers.product_mapper import ProductMapper

class ProductRepository:

    def __init__(self, database):
        self.database = database

    def create_table(self):
        self.database.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                barcode TEXT UNIQUE NOT NULL,

                name TEXT NOT NULL,

                category TEXT,

                purchase_price REAL NOT NULL,

                selling_price REAL NOT NULL,

                quantity INTEGER NOT NULL DEFAULT 0,

                minimum_stock INTEGER DEFAULT 5,

                created_at TEXT,

                updated_at TEXT
            )
        """)

    def add_product(self, product):
        self.database.cursor.execute("""
            INSERT INTO products (
                barcode,
                name,
                category,
                purchase_price,
                selling_price,
                quantity,
                minimum_stock,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product.barcode,
            product.name,
            product.category,
            product.purchase_price,
            product.selling_price,
            product.quantity,
            product.minimum_stock,
            product.created_at,
            product.updated_at
        ))

    def get_all_products(self):

        rows = self.database.cursor.execute(
            "SELECT * FROM products"
        ).fetchall()

        return [
            ProductMapper.from_row(row)
            for row in rows
        ]


    def get_by_id(self, product_id: int):
        query = """
            SELECT *
             FROM products
            WHERE id = ?
        """

        self.database.cursor.execute(query, (product_id,))
        row = self.database.cursor.fetchone()

        if row is None:
            return None

        return ProductMapper.from_row(row)
    
    def get_by_barcode(self, barcode: str):
        query = """
            SELECT *
            FROM products
            WHERE barcode = ?
        """
        self.database.cursor.execute(query, (barcode,))
        row = self.database.cursor.fetchone()

        if row is None:
            return None

        return ProductMapper.from_row(row)

    def search(self, keyword: str):
        like_keyword = f"%{keyword}%"

        query = """
            SELECT *
            FROM products
            WHERE name LIKE ?
            OR barcode LIKE ?
            OR category LIKE ?
        """

        self.database.cursor.execute(
            query,
            (like_keyword, like_keyword, like_keyword)
        )

        rows = self.database.cursor.fetchall()

        return [
            ProductMapper.from_row(row)
            for row in rows
        ]

    def update_product(self, product):
        query = """
            UPDATE products
            SET barcode = ?,
                name = ?,
                category = ?,
                purchase_price = ?,
                selling_price = ?,
                quantity = ?,
                minimum_stock = ?,
                updated_at = ?
            WHERE id = ?
        """
        self.database.cursor.execute(
            query,
            (
                product.barcode,
                product.name,
                product.category,
                product.purchase_price,
                product.selling_price,
                product.quantity,
                product.minimum_stock,
                datetime.now().isoformat(),
                product.id
            )
        )
    
    def decrease_stock(self, product_id: int, quantity: int):
        """
        Decrease the stock of a product.

        Raises:
            ValueError: if the product does not exist.
            ValueError: if there is not enough stock.
        """

        product = self.get_by_id(product_id)

        if product is None:
            raise ValueError("Product not found.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if product.quantity < quantity:
            raise ValueError(
                f"Insufficient stock for '{product.name}'. "
                f"Available: {product.quantity}"
            )

        new_quantity = product.quantity - quantity

        query = """
            UPDATE products
            SET quantity = ?,
                updated_at = ?
            WHERE id = ?
        """

        self.database.cursor.execute(
            query,
            (
                new_quantity,
                datetime.now().isoformat(),
                product_id
            )
        )

        return new_quantity
