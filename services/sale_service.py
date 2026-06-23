from utils.ticket_printer import TicketPrinter
from utils.thermal_printer import ThermalPrinter
from datetime import datetime, timedelta


class SaleService:
    """
    Business logic for handling sales.
    """

    def __init__(self, sale_repository, product_repository):
        self.sale_repository = sale_repository
        self.product_repository = product_repository

        self.database = sale_repository.db

        self.current_sale_id = None

        self.last_completed_sale_id = None
        self.last_ticket = None
        self.ticket_printer = TicketPrinter()
        self.thermal_printer = ThermalPrinter(mode="usb")

    # =========================
    # START SALE
    # =========================
    def start_sale(self):
        """
        Create a new sale and keep its id in memory.
        """
        self.current_sale_id = self.sale_repository.create_sale()
        return self.current_sale_id

    # =========================
    # ADD PRODUCT TO SALE
    # =========================
    def add_product(self, product_id, quantity):
        """
        Add a product to the current sale.
        """

        if self.current_sale_id is None:
            raise Exception("No active sale. Start a sale first.")

        product = self.product_repository.get_by_id(product_id)

        if not product:
            product = self.product_repository.get_by_barcode(product_id)

        unit_price = product.selling_price
        product_name = product.name

        self.sale_repository.add_item(
            sale_id=self.current_sale_id,
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            unit_price=unit_price
        )

        # update total dynamically
        self.recalculate_total()

    # =========================
    # RECALCULATE TOTAL
    # =========================
    def recalculate_total(self):
        """
        Recalculate sale total from DB items.
        """

        items = self.sale_repository.get_sale_items(self.current_sale_id)

        total = sum(item["subtotal"] for item in items)

        self.sale_repository.update_total(self.current_sale_id, total)

        return total

    # =========================
    # GET CURRENT SALE SUMMARY
    # =========================
    def get_current_sale(self):
        """
        Return current sale with items.
        """

        if self.current_sale_id is None:
            return None

        sale = self.sale_repository.get_sale(self.current_sale_id)
        items = self.sale_repository.get_sale_items(self.current_sale_id)

        return {
            "sale": sale,
            "items": items,
        }
    
    def update_item_quantity(
        self,
        product_id,
        new_quantity
    ):
        """
        Update the quantity of an item in the current sale.
        """

        if self.current_sale_id is None:
            raise Exception("No active sale.")

        if new_quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        sale_item = self.sale_repository.get_sale_item(
            self.current_sale_id,
            product_id
        )

        if sale_item is None:
            raise ValueError(
                "Product is not in the current sale."
            )

        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ValueError(
                "Product not found."
            )

        if new_quantity > product.quantity:
            raise ValueError(
                f"Insufficient stock. Available: {product.quantity}"
            )

        subtotal = new_quantity * sale_item["unit_price"]

        self.sale_repository.update_item_quantity(
            self.current_sale_id,
            product_id,
            new_quantity,
            subtotal
        )
        return self.recalculate_total()
    
    def remove_item(self, product_id):
        """
        Remove a product from current sale.
        """

        if self.current_sale_id is None:
            raise Exception("No active sale.")

        sale_item = self.sale_repository.get_sale_item(
            self.current_sale_id,
            product_id
        )

        if sale_item is None:
            raise ValueError("Product not in current sale.")

        self.sale_repository.delete_item(
            self.current_sale_id,
            product_id
        )

        return self.recalculate_total()
    
    def cancel_sale(self):
        """
        Cancel current sale completely.
        """

        if self.current_sale_id is None:
            raise Exception("No active sale.")

        try:
            # delete from DB
            self.sale_repository.delete_sale(self.current_sale_id)

            # reset state
            self.current_sale_id = None

            return True

        except Exception as e:
            raise e

    # =========================
    # END SALE
    # =========================
    def end_sale(self):
        """
        Finalize sale safely with stock update.
        """

        if self.current_sale_id is None:
            raise Exception("No active sale.")

        try:
            # 1. récupérer les items
            items = self.sale_repository.get_sale_items(
                self.current_sale_id
            )

            if not items:
                raise Exception("Cannot finalize empty sale.")

            # 2. vérifier le stock + décrémenter
            for item in items:
                self.product_repository.decrease_stock(
                    item["product_id"],
                    item["quantity"]
                )
            # 3. calculer et enregistrer le total
            total = self.recalculate_total()

            # 4. marquer la vente comme terminée
            self.sale_repository.complete_sale(
                self.current_sale_id
            )

            # 5. valider toute la transaction
            self.database.commit()

            # 6. mémoriser la dernière vente terminée
            self.last_completed_sale_id = self.current_sale_id

            # 7. fermer la vente courante
            self.current_sale_id = None
            return total

        except Exception as e:
            self.database.rollback()
            raise e
        
    def get_sales_history(self):
        """
        Return all completed sales.
        """
        return self.sale_repository.get_completed_sales()
    
    def generate_receipt(self):
        """
        Generate receipt for last completed sale.
        """

        if self.last_completed_sale_id is None:
            raise Exception("No completed sale available.")

        sale = self.sale_repository.get_sale(
            self.last_completed_sale_id
        )

        items = self.sale_repository.get_sale_items(
            self.last_completed_sale_id
        )

        return self.ticket_printer.generate(
            sale,
            items
        )
    
    def generate_last_ticket(self):
        if self.last_completed_sale_id is None:
            raise Exception("No completed sale available.")

        sale = self.sale_repository.get_sale(self.last_completed_sale_id)
        items = self.sale_repository.get_sale_items(self.last_completed_sale_id)

        self.last_ticket = self.ticket_printer.generate(sale, items)

        return self.last_ticket
    
    def reprint_last_ticket(self):
        """
        Reprint the last generated receipt.
        """

        if self.last_ticket is None:
            raise Exception("No ticket available.")

        self.thermal_printer.print_receipt(
            self.last_ticket
        )

        return self.last_ticket
    
    
    def get_sale_details(self, sale_id):
        data = self.sale_repository.get_sale_with_items(sale_id)

        if not data["sale"]:
            raise Exception("Sale not found")

        return data
    
    def print_last_ticket(self):
        """
        Print the last generated receipt.
        """

        if self.last_ticket is None:
            raise Exception("No ticket available.")

        self.thermal_printer.print_receipt(
            self.last_ticket
        )

    # =========================
    # ACCOUNTING CORE
    # =========================

    def get_sales_between(self, start_date, end_date):
        """
        Return completed sales between two dates (inclusive).
        """
        sales = self.sale_repository.get_completed_sales()

        filtered_sales = []

        for sale in sales:
            sale_date = datetime.fromisoformat(
                sale["created_at"]
            )

            if start_date <= sale_date <= end_date:
                filtered_sales.append(sale)

        return filtered_sales

    def get_sales_total(self, sales):
        """
        Calculate total revenue from a sales list.
        """
        return sum(sale["total"] for sale in sales)

    def get_sales_count(self, sales):
        """
        Return number of sales.
        """
        return len(sales)

    # =========================
    # DAILY REPORT
    # =========================

    def get_today_sales(self):
        """
        Return today's completed sales.
        """
        now = datetime.now()

        start = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        end = now

        return self.get_sales_between(start, end)

    def get_today_total(self):
        """
        Return today's revenue.
        """
        return self.get_sales_total(
            self.get_today_sales()
        )

    def get_today_sales_count(self):
        """
        Return today's number of sales.
        """
        return self.get_sales_count(
            self.get_today_sales()
        )
    def get_daily_report(self):
        """
        Return today's accounting report.
        """

        sales = self.get_today_sales()

        return {
            "title": "DAILY REPORT",
            "period": datetime.now().strftime("%d/%m/%Y"),
            "sales_count": self.get_sales_count(sales),
            "revenue": self.get_sales_total(sales)
        }
    
    
    # =========================
    # WEEKLY REPORT
    # =========================

    def get_week_sales(self):
        """
        Return completed sales for the current week.
        Week starts on Monday.
        """
        now = datetime.now()

        start = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        start = start.replace(
            day=now.day
        ) - timedelta(days=now.weekday())

        end = now

        return self.get_sales_between(start, end)

    def get_week_total(self):
        """
        Return weekly revenue.
        """
        return self.get_sales_total(
            self.get_week_sales()
        )

    def get_week_sales_count(self):
        """
        Return weekly number of sales.
        """
        return self.get_sales_count(
            self.get_week_sales()
        )
    def get_weekly_report(self):
        """
        Return weekly accounting report.
        """

        now = datetime.now()

        start = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        ) - timedelta(days=now.weekday())

        end = now

        sales = self.get_sales_between(start, end)

        period = (
            f"{start.strftime('%d/%m/%Y')} → "
            f"{end.strftime('%d/%m/%Y')}"
        )

        return {
            "title": "WEEKLY REPORT",
            "period": period,
            "sales_count": self.get_sales_count(sales),
            "revenue": self.get_sales_total(sales)
        }
    def get_month_sales(self):
        """
        Return completed sales for the current month.
        """
        now = datetime.now()

        start = now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
        end = now
        return self.get_sales_between(start, end)
    
    def get_month_total(self):
        """
        Return monthly revenue.
        """
        return self.get_sales_total(
            self.get_month_sales()
        )
    
    def get_month_sales_count(self):
        """
        Return monthly number of sales.
        """
        return self.get_sales_count(
            self.get_month_sales()
        )
    
    def get_monthly_report(self):

        now = datetime.now()

        start = now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        end = now

        sales = self.get_sales_between(start, end)

        period = now.strftime("%B %Y")  # ex: June 2026

        return {
            "title": "MONTHLY REPORT",
            "period": period,
            "sales_count": self.get_sales_count(sales),
            "revenue": self.get_sales_total(sales)
        }
    
    def get_profit_for_sales(self, sales):
        """
        Calculate real profit from sales using product purchase price.
        """

        total_revenue = 0
        total_cost = 0

        for sale in sales:
            items = self.sale_repository.get_sale_items(sale["id"])

            for item in items:
                product = self.product_repository.get_by_id(item["product_id"])

                if not product:
                    continue

                revenue = item["subtotal"]

                # coût réel basé sur purchase_price
                cost = product.purchase_price * item["quantity"]

                total_revenue += revenue
                total_cost += cost

        return {
            "revenue": total_revenue,
            "cost": total_cost,
            "profit": total_revenue - total_cost
        }
    
    def get_profit_report(self):
        """
        Return profit report for all completed sales.
        """

        sales = self.sale_repository.get_completed_sales()
        data = self.get_profit_for_sales(sales)

        return {
            "title": "PROFIT REPORT",
            "period": "All time",
            "sales_count": self.get_sales_count(sales),
            "revenue": data["revenue"],
            "cost": data["cost"],
            "profit": data["profit"]
        }
    
    def get_today_profit_report(self):
        """
        Profit report for today.
        """

        sales = self.get_today_sales()
        data = self.get_profit_for_sales(sales)

        return {
            "title": "PROFIT REPORT (TODAY)",
            "period": datetime.now().strftime("%d/%m/%Y"),
            "revenue": data["revenue"],
            "cost": data["cost"],
            "profit": data["profit"]
        }
    
    #STOCK VALUETION
    def get_stock_valuation(self):
        """
        Calculate total value of current stock.
        """

        products = self.product_repository.get_all_products()

        total_value = 0

        for product in products:
            total_value += product.purchase_price * product.quantity

        return {
            "title": "STOCK VALUATION",
            "total_value": total_value,
            "products_count": len(products)
        }
    
    def get_stock_valuation_details(self):
        """
        Return stock value per product.
        """

        products = self.product_repository.get_all_products()

        details = []

        total = 0

        for p in products:
            value = p.purchase_price * p.quantity

            details.append({
                "name": p.name,
                "quantity": p.quantity,
                "unit_cost": p.purchase_price,
                "value": value
            })

            total += value

        return {
            "title": "STOCK VALUATION DETAIL",
            "items": details,
            "total_value": total
        }
    
    #TOP SELLING PRODUCT
    def get_top_selling_products(self, limit=10):
        """
        Return most sold products based on quantity sold.
        """

        sales = self.sale_repository.get_completed_sales()

        product_sales = {}

        for sale in sales:
            items = self.sale_repository.get_sale_items(sale["id"])

            for item in items:
                product_id = item["product_id"]
                quantity = item["quantity"]

                if product_id not in product_sales:
                    product_sales[product_id] = 0

                product_sales[product_id] += quantity

        # transform into list
        result = []

        for product_id, total_qty in product_sales.items():
            product = self.product_repository.get_by_id(product_id)

            if product:
                result.append({
                    "id": product.id,
                    "name": product.name,
                    "quantity_sold": total_qty,
                    "revenue": total_qty * product.selling_price
                })

        # sort by quantity sold
        result.sort(key=lambda x: x["quantity_sold"], reverse=True)

        return result[:limit]
    
    #UNSOLD PRODUCT
    def get_unsold_products(self):
        """
        Return products that have never been sold.
        """

        all_products = self.product_repository.get_all_products()
        sales = self.sale_repository.get_completed_sales()

        sold_ids = set()

        for sale in sales:
            items = self.sale_repository.get_sale_items(sale["id"])

            for item in items:
                sold_ids.add(item["product_id"])

        return [
            product
            for product in all_products
            if product.id not in sold_ids
        ]
    def get_top_selling_report(self):
        return {
            "title": "TOP SELLING PRODUCTS",
            "items": self.get_top_selling_products()
        }


    def get_unsold_report(self):
        return {
            "title": "UNSOLD PRODUCTS",
            "items": self.get_unsold_products()
        }
