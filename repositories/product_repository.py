"""inventory management repository module"""

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
        self.database.commit()

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
        self.database.commit()

    def get_all_products(self):

        rows = self.database.cursor.execute(
            "SELECT * FROM products"
        ).fetchall()

        return [
            ProductMapper.from_row(row)
            for row in rows
        ]
