import csv
import os
from datetime import datetime


class ExportService:
    """
    Handles CSV export for products, sales, etc.
    """

    def __init__(self, database):
        self.database = database

    # =========================
    # EXPORT PRODUCTS
    # =========================
    def export_products(self, file_path="exports/products.csv"):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        rows = self.database.cursor.execute(
            "SELECT * FROM products"
        ).fetchall()

        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=';')

            writer.writerow([
                "ID", "Barcode", "Name", "Category",
                "Purchase Price", "Selling Price",
                "Quantity", "Min Stock"
            ])

            for r in rows:
                writer.writerow([
                    r["id"],
                    r["barcode"],
                    r["name"],
                    r["category"],
                    r["purchase_price"],
                    r["selling_price"],
                    r["quantity"],
                    r["minimum_stock"]
                ])

        return file_path

    # =========================
    # EXPORT SALES
    # =========================
    def export_sales(self, file_path="exports/sales.csv"):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        rows = self.database.cursor.execute(
            "SELECT * FROM sales"
        ).fetchall()

        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=';')

            writer.writerow([
                "ID", "Date", "Total", "Status"
            ])

            for r in rows:
                writer.writerow([
                    r["id"],
                    r["created_at"],
                    r["total"],
                    r["status"]
                ])

        return file_path
