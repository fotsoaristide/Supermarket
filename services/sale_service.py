class SaleService:
    """
    Business logic for handling sales.
    """

    def __init__(self, sale_repository, product_repository):
        self.sale_repository = sale_repository
        self.product_repository = product_repository

        self.database = sale_repository.db

        self.current_sale_id = None

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
            items = self.sale_repository.get_sale_items(self.current_sale_id)

            if not items:
                raise Exception("Cannot finalize empty sale.")

            # 2. vérifier stock + décrémenter
            for item in items:
                self.product_repository.decrease_stock(
                    item["product_id"],
                    item["quantity"]
                )

            # 3. marquer vente comme terminée
            self.sale_repository.complete_sale(self.current_sale_id)

            # 4. commit global
            self.database.commit()

            total = self.recalculate_total()

            # 5. reset session
            self.current_sale_id = None

            return total

        except Exception as e:
            self.database.rollback()
            raise e