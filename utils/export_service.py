import csv
import os
from datetime import datetime


class ExportService:
    """
    Handles CSV export for products, sales, etc.
    """

    def __init__(self, database):
        self.database = database
    
    def write_report_header(
        self,
        writer,
        title
    ):
        writer.writerow([title])
        writer.writerow([
            "Generated At",
            datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        ])
        writer.writerow([])

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
    def export_sales(
        self,
        file_path="exports/sales.csv"
    ):
        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        rows = self.database.cursor.execute(
            """
            SELECT *
            FROM sales
            ORDER BY id DESC
            """
        ).fetchall()

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(
                file,
                delimiter=';'
            )

            self.write_report_header(
                writer,
                "SALES HISTORY REPORT"
            )

            writer.writerow([
                "Sale ID",
                "Date",
                "Payment",
                "Discount",
                "Total",
                "Status"
            ])

            for r in rows:

                writer.writerow([
                    r["id"],
                    r["created_at"],
                    r["payment_method"],
                    r["discount"],
                    r["total"],
                    r["status"]
                ])

        return file_path
    
    def export_profit_report(
        self,
        sale_service,
        file_path="exports/profit_report.csv"
    ):

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        report = sale_service.get_profit_report()

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(
                file,
                delimiter=';'
            )

            self.write_report_header(
                writer,
                "PROFIT REPORT"
            )

            writer.writerow([
                "Period",
                "Revenue",
                "Cost",
                "Profit"
            ])

            writer.writerow([
                report["period"],
                report["revenue"],
                report["cost"],
                report["profit"]
            ])

        return file_path
    
    def export_top_products(
        self,
        sale_service,
        file_path="exports/top_products.csv"
    ):

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        products = sale_service.get_top_selling_products()

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(
                file,
                delimiter=';'
            )

            self.write_report_header(
                writer,
                "TOP SELLING PRODUCTS"
            )

            writer.writerow([
                "Rank",
                "Product",
                "Quantity Sold",
                "Revenue"
            ])

            rank = 1

            for p in products:

                writer.writerow([
                    rank,
                    p["name"],
                    p["quantity_sold"],
                    p["revenue"]
                ])

                rank += 1

        return file_path
    
    def export_unsold_products(
        self,
        sale_service,
        file_path="exports/unsold_products.csv"
    ):

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        products = sale_service.get_unsold_products()

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(
                file,
                delimiter=';'
            )

            self.write_report_header(
                writer,
                "UNSOLD PRODUCTS"
            )

            writer.writerow([
                "Barcode",
                "Product",
                "Quantity",
                "Purchase Price",
                "Selling Price"
            ])

            for p in products:

                writer.writerow([
                    p.barcode,
                    p.name,
                    p.quantity,
                    p.purchase_price,
                    p.selling_price
                ])

        return file_path
    
    def export_stock_valuation(
        self,
        sale_service,
        file_path="exports/stock_valuation.csv"
    ):

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        report = sale_service.get_stock_valuation_details()

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(
                file,
                delimiter=';'
            )

            self.write_report_header(
                writer,
                "STOCK VALUATION REPORT"
            )

            writer.writerow([
                "Product",
                "Quantity",
                "Unit Cost",
                "Inventory Value"
            ])

            for item in report["items"]:

                writer.writerow([
                    item["name"],
                    item["quantity"],
                    item["unit_cost"],
                    item["value"]
                ])

            writer.writerow([])

            writer.writerow([
                "TOTAL",
                "",
                "",
                report["total_value"]
            ])

        return file_path
    
    def export_sales_history(
        self,
        sale_service,
        file_path="exports/sales_history.csv"
    ):

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        sales = sale_service.get_sales_history()

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(
                file,
                delimiter=';'
            )

            self.write_report_header(
                writer,
                "SALES HISTORY"
            )

            writer.writerow([
                "Sale ID",
                "Date",
                "Payment",
                "Total"
            ])

            for sale in sales:

                writer.writerow([
                    sale["id"],
                    sale["created_at"],
                    sale["payment_method"],
                    sale["total"]
                ])

        return file_path
    
    def export_sale_a4(
        self,
        sale,
        items,
        file_path
    ):
        import os
        from datetime import datetime

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        dt = datetime.fromisoformat(
            sale["created_at"]
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write("=" * 52 + "\n")
            f.write("               NB MINI-MARKET\n")
            f.write("              Souza - Cameroun\n")
            f.write("       Votre mini-market de confiance\n")
            f.write("            Tel : +237 682 454 030\n")
            f.write("=" * 52 + "\n\n")

            f.write(f"FACTURE N° : {sale['id']}\n")
            f.write(
                f"DATE       : "
                f"{dt.strftime('%d/%m/%Y')}\n"
            )

            f.write(
                f"HEURE      : "
                f"{dt.strftime('%H:%M')}\n"
            )

            f.write(
                f"PAIEMENT   : "
                f"{sale['payment_method']}\n\n"
            )

            f.write("-" * 52 + "\n")
            f.write(
                f"{'ARTICLE':20}"
                f"{'QTE':>6}"
                f"{'PU':>10}"
                f"{'TOTAL':>12}\n"
            )
            f.write("-" * 52 + "\n")

            for item in items:

                f.write(
                    f"{item['product_name'][:20]:20}"
                    f"{item['quantity']:>6}"
                    f"{item['unit_price']:>10.0f}"
                    f"{item['subtotal']:>12.0f}\n"
                )

            f.write("\n")
            f.write("-" * 52 + "\n")

            f.write(
                f"{'SOUS TOTAL :':30}"
                f"{sale['total']:>20.0f} FCFA\n"
            )

            f.write(
                f"{'REMISE :':30}"
                f"{sale['discount']:>20.0f} FCFA\n"
            )

            f.write("\n")

            f.write(
                f"{'TOTAL :':30}"
                f"{sale['total']:>20.0f} FCFA\n"
            )

            f.write("\n")
            f.write("=" * 52 + "\n")
            f.write("           Merci pour votre achat\n")
            f.write("           Conservez cette facture\n")
            f.write("=" * 52 + "\n")

        return file_path
