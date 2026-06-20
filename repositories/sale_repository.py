from datetime import datetime


class SaleRepository:
    """Handles database operations for sales."""

    def __init__(self, database):
        self.db = database

    # =========================
    # CREATE SALE
    # =========================
    def create_sale(self):
        query = """
        INSERT INTO sales (created_at, total, status, payment_method, discount)
        VALUES (?, ?, ?, ?, ?)
        """

        params = (
            datetime.now().isoformat(),
            0.0,
            "IN_PROGRESS",
            "CASH",
            0.0
        )

        self.db.cursor.execute(query, params)

        return self.db.cursor.lastrowid

    # =========================
    # ADD ITEM TO SALE
    # =========================
    def add_item(self, sale_id, product_id, product_name, quantity, unit_price):
        subtotal = quantity * unit_price

        query = """
        INSERT INTO sale_items (
            sale_id, product_id, product_name,
            quantity, unit_price, subtotal
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """

        self.db.cursor.execute(
            query,
            (
                sale_id,
                product_id,
                product_name,
                quantity,
                unit_price,
                subtotal
            )
        )

    # =========================
    # GET SALE ITEMS
    # =========================
    def get_sale_items(self, sale_id):
        query = """
        SELECT * FROM sale_items WHERE sale_id = ?
        """

        self.db.cursor.execute(query, (sale_id,))
        rows = self.db.cursor.fetchall()

        return rows

    # =========================
    # GET SALE
    # =========================
    def get_sale(self, sale_id):
        query = """
        SELECT * FROM sales WHERE id = ?
        """

        self.db.cursor.execute(query, (sale_id,))
        row = self.db.cursor.fetchone()

        return row

    # =========================
    # UPDATE TOTAL
    # =========================
    def update_total(self, sale_id, total):
        query = """
        UPDATE sales SET total = ? WHERE id = ?
        """

        self.db.cursor.execute(query, (total, sale_id))

    def complete_sale(self, sale_id):
        query = """
            UPDATE sales
            SET status = ?
            WHERE id = ?
        """

        self.db.cursor.execute(
            query,
            (
                "COMPLETED",
                sale_id
            )
        )
