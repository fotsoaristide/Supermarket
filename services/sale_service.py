from utils.ticket_printer import TicketPrinter
from utils.thermal_printer import ThermalPrinter


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
    

    def get_sale_history(self):
        return self.sale_repository.get_completed_sales()
    
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
