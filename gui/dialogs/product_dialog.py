import customtkinter as ctk
from models.product import Product
from gui.theme import Theme


class ProductDialog(ctk.CTkToplevel):
    """
    POS-style dialog for creating products.
    Builds a real Product model and sends it to controller.
    """

    def __init__(
                self,
                master,
                ui,
                product=None,
                edit_mode=False
        ):

        super().__init__(master)

        self.ui = ui
        self.product = product
        self.edit_mode = edit_mode

        if edit_mode:
            self.title("Update Product")
        else:
            self.title("Add Product")

        self.geometry("420x500")
        self.grab_set()

        self.build_ui()

        if self.edit_mode and self.product:
            self.load_product()

    def build_ui(self):

        # =========================
        # FORM FIELDS
        # =========================

        self.barcode = ctk.CTkEntry(self, placeholder_text="Barcode")
        self.barcode.pack(fill="x", padx=20, pady=8)

        self.name = ctk.CTkEntry(self, placeholder_text="Name")
        self.name.pack(fill="x", padx=20, pady=8)

        self.category = ctk.CTkEntry(self, placeholder_text="Category")
        self.category.pack(fill="x", padx=20, pady=8)

        self.purchase_price = ctk.CTkEntry(self, placeholder_text="Purchase Price")
        self.purchase_price.pack(fill="x", padx=20, pady=8)

        self.selling_price = ctk.CTkEntry(self, placeholder_text="Selling Price")
        self.selling_price.pack(fill="x", padx=20, pady=8)

        self.quantity = ctk.CTkEntry(self, placeholder_text="Quantity")
        self.quantity.pack(fill="x", padx=20, pady=8)

        self.minimum_stock = ctk.CTkEntry(self, placeholder_text="Minimum Stock")
        self.minimum_stock.insert(0, "5")
        self.minimum_stock.pack(fill="x", padx=20, pady=8)

        # =========================
        # SAVE BUTTON
        # =========================

        button_text = (
            "Update Product"
            if self.edit_mode
            else "Save Product"
        )

        self.save_btn = ctk.CTkButton(
            self,
            text=button_text,
            fg_color=Theme.PRIMARY,
            command=self.save_product
        )

        self.save_btn.pack(
            pady=20
        )
    
    def load_product(self):

        self.barcode.insert(
            0,
            self.product["barcode"]
        )

        self.name.insert(
            0,
            self.product["name"]
        )

        self.category.insert(
            0,
            self.product.get("category", "")
        )

        self.purchase_price.insert(
            0,
            str(
                self.product.get(
                    "purchase_price",
                    0
                )
            )
        )

        self.selling_price.insert(
            0,
            str(
                self.product["price"]
            )
        )

        self.quantity.insert(
            0,
            str(
                self.product["stock"]
            )
        )

        self.minimum_stock.delete(0, "end")

        self.minimum_stock.insert(
            0,
            str(
                self.product.get(
                    "minimum_stock",
                    5
                )
            )
        )

    def save_product(self):

        if getattr(self, "saving", False):
            return

        self.saving = True

        try:

            product = Product(

                id=(
                    self.product["id"]
                    if self.edit_mode
                    else None
                ),

                barcode=self.barcode.get(),

                name=self.name.get(),

                category=self.category.get(),

                purchase_price=float(
                    self.purchase_price.get()
                ),

                selling_price=float(
                    self.selling_price.get()
                ),

                quantity=int(
                    self.quantity.get()
                ),

                minimum_stock=int(
                    self.minimum_stock.get() or 5
                )
            )

            if self.edit_mode:

                confirm = ctk.CTkToplevel(self)
                confirm.title("Confirm Update")
                confirm.geometry("300x150")
                confirm.grab_set()

                result = {"ok": False}

                ctk.CTkLabel(
                    confirm,
                    text=f"Update\n\n{product.name} ?"
                ).pack(expand=True, pady=20)

                def yes():
                    result["ok"] = True
                    confirm.destroy()

                def no():
                    confirm.destroy()

                buttons = ctk.CTkFrame(confirm)
                buttons.pack(fill="x", padx=15, pady=10)

                ctk.CTkButton(
                    buttons,
                    text="YES",
                    command=yes
                ).pack(side="left", expand=True, fill="x", padx=5)

                ctk.CTkButton(
                    buttons,
                    text="NO",
                    command=no
                ).pack(side="left", expand=True, fill="x", padx=5)

                confirm.wait_window()

                if not result["ok"]:
                    self.saving = False
                    return

                self.ui.product_controller.update_product_from_model(
                    product
                )

            else:

                self.ui.product_controller.add_product_from_model(
                    product
                )

            self.destroy()

        except Exception as e:
            print(
                "Product dialog error:",
                e
            )

        finally:
            self.saving = False
