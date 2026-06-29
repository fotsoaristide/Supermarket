import customtkinter as ctk
from gui.views.base_view import BaseView
from gui.theme import Theme
import platform


class SalesView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Sales")

        self.ui = ui
        self.sale_service = self.ui.sale_service

        self.current_sale = None
        self.is_processing = False
        self.last_receipt = None
        self.receipt_window = None

        self.build_ui()
        self.start_new_sale()

        self.ui.event_bus.subscribe(
            "sale_changed",
            lambda _: self.refresh_cart()
        )

        self.ui.event_bus.subscribe(
            "stock_updated",
            lambda _: self.load_products()
        )

        self.ui.event_bus.subscribe(
            "product_changed",
            lambda _: self.load_products()
        )

        self.after(150, self.focus_scan)

    # =========================
    # UI
    # =========================
    def build_ui(self):

        self.container = ctk.CTkFrame(self.body, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.grid_columnconfigure(0, weight=1, uniform="col")
        self.container.grid_columnconfigure(1, weight=2, uniform="col")

        self.container.grid_rowconfigure(0, weight=1)

        # LEFT PANEL
        self.left_panel = ctk.CTkFrame(self.container, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.left_panel.grid_rowconfigure(1, weight=1)
        self.left_panel.grid_columnconfigure(0, weight=1)

        self.scan_var = ctk.StringVar()

        self.scan_entry = ctk.CTkEntry(
            self.left_panel,
            textvariable=self.scan_var,
            placeholder_text="Scan barcode + ENTER"
        )
        self.scan_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.scan_entry.bind("<Return>", self.on_enter_scan)
        self.scan_var.trace_add("write", self.on_scan)

        self.products_list = ctk.CTkScrollableFrame(self.left_panel)
        self.products_list.grid(row=1, column=0, sticky="nsew", padx=10)

        # RIGHT PANEL
        self.right_panel = ctk.CTkFrame(self.container, fg_color=Theme.SURFACE)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=0)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.cart_items_frame = ctk.CTkScrollableFrame(self.right_panel)
        self.cart_items_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.footer = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.footer.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.total_label = ctk.CTkLabel(
            self.footer,
            text="TOTAL: 0 FCFA",
            font=Theme.SUBTITLE,
            text_color=Theme.PRIMARY
        )
        self.total_label.pack(side="left")

        self.actions_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.actions_frame.pack(side="right")

        self.receipt_btn = ctk.CTkButton(
            self.actions_frame,
            text="RECEIPT",
            width=90,
            command=self.show_receipt
        )
        self.receipt_btn.pack(side="left", padx=3)

        self.reprint_btn = ctk.CTkButton(
            self.actions_frame,
            text="REPRINT",
            width=90,
            command=self.reprint_ticket
        )
        self.reprint_btn.pack(side="left", padx=3)

        self.print_toggle_btn = ctk.CTkButton(
            self.actions_frame,
            text="PRINT ON",
            width=90,
            fg_color="#16a34a",
            command=self.toggle_printing
        )
        self.print_toggle_btn.pack(side="left", padx=3)

        self.cancel_btn = ctk.CTkButton(
            self.footer,
            text="CANCEL",
            width=120,
            fg_color="#dc2626",
            command=self.cancel_sale
        )
        self.cancel_btn.pack(side="right", padx=5)

        self.checkout_btn = ctk.CTkButton(
            self.footer,
            text="CHECKOUT",
            width=120,
            fg_color=Theme.SUCCESS,
            command=self.checkout
        )
        self.checkout_btn.pack(side="right", padx=5)

        self.render_products()
        self.refresh_cart()

    # =========================
    # PAYMENT MODAL (CASH PRO FIXED)
    # =========================
    def open_cash_payment_modal(self):
        """
        Payment modal corrigé:
        - quick amounts mis à jour
        - suppression incohérence FCFA FCFA
        """

        data = self.sale_service.get_current_sale()

        if not data or not data["items"]:
            return

        total = sum(item["subtotal"] for item in data["items"])

        win = ctk.CTkToplevel(self)
        win.title("Cash Payment")

        win.update_idletasks()

        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()

        width = 520
        height = 650

        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)

        win.geometry(f"{width}x{height}+{x}+{y}")

        win.grab_set()
        win.focus_force()

        # =========================
        # TITLE
        # =========================
        ctk.CTkLabel(
            win,
            text="CASH PAYMENT",
            font=("Arial", 22, "bold"),
            text_color=Theme.PRIMARY
        ).pack(pady=(20, 10))

        # =========================
        # TOTAL (FIX FCFA DUPLICATION SAFE)
        # =========================
        ctk.CTkLabel(
            win,
            text=f"TOTAL: {self.format_price(total)} FCFA",
            font=("Arial", 24, "bold"),
            text_color=Theme.PRIMARY
        ).pack(pady=15)

        cash_var = ctk.StringVar()

        cash_entry = ctk.CTkEntry(
            win,
            textvariable=cash_var,
            placeholder_text="Cash received",
            height=50,
            font=("Arial", 22)
        )
        cash_entry.pack(fill="x", padx=30, pady=10)

        change_label = ctk.CTkLabel(
            win,
            text="CHANGE: 0 FCFA",
            font=("Arial", 20, "bold")
        )
        change_label.pack(pady=10)

        # =========================
        # QUICK BUTTONS (UPDATED)
        # =========================
        quick_frame = ctk.CTkFrame(win, fg_color="transparent")
        quick_frame.pack(pady=20)

        def set_cash(amount):
            cash_var.set(str(amount))
            cash_entry.focus_set()

        quick_values = [
            500,
            1000,
            2000,
            5000,
            10000
        ]

        for value in quick_values:
            ctk.CTkButton(
                quick_frame,
                text=self.format_price(value),
                width=80,
                command=lambda v=value: set_cash(v)
            ).pack(side="left", padx=5)

        def update_change(*_):
            try:
                cash = float(cash_var.get())
            except:
                change_label.configure(text="CHANGE: 0 FCFA")
                return

            change = cash - total

            if change < 0:
                change_label.configure(text="INSUFFICIENT CASH")
            else:
                change_label.configure(
                    text=f"CHANGE: {self.format_price(change)} FCFA"
                )

        cash_var.trace_add("write", update_change)

        def confirm_payment():
            try:
                cash = float(cash_var.get())
            except:
                return

            if cash < total:
                return

            self.is_processing = True

            try:
                self.sale_service.end_sale()
                self.last_receipt = self.sale_service.generate_last_ticket()

                try:
                    self.sale_service.print_last_ticket()
                except:
                    pass

                self.ui.event_bus.emit("sale_changed")
                self.ui.event_bus.emit("sale_completed")

                self.start_new_sale()
                self.refresh_cart()

                self.scan_var.set("")
                self.focus_scan()

                win.destroy()

            except Exception as e:
                print("Payment error:", e)

            finally:
                self.is_processing = False

        actions = ctk.CTkFrame(win, fg_color="transparent")
        actions.pack(side="bottom", fill="x", padx=30, pady=20)

        ctk.CTkButton(
            actions,
            text="CONFIRM PAYMENT",
            fg_color=Theme.SUCCESS,
            height=45,
            command=confirm_payment
        ).pack(side="left", expand=True, fill="x", padx=5)

        ctk.CTkButton(
            actions,
            text="CANCEL",
            fg_color="#dc2626",
            height=45,
            command=win.destroy
        ).pack(side="left", expand=True, fill="x", padx=5)

        win.bind("<Return>", lambda e: confirm_payment())
        win.bind("<Escape>", lambda e: win.destroy())

    # =========================
    # SCAN + CART (UNCHANGED CORE)
    # =========================
    def focus_scan(self):
        try:
            self.scan_entry.focus_set()
        except:
            pass

    def on_enter_scan(self, event=None):
        query = self.scan_var.get().strip()

        if not query:
            return

        self.beep()

        products = self.load_products()

        for p in products:
            if query == p.barcode:
                self.add_to_cart(p.id)
                self.scan_var.set("")
                return

        for p in products:
            if query.lower() in p.name.lower():
                self.add_to_cart(p.id)
                self.scan_var.set("")
                return

    def on_scan(self, *_):
        q = self.scan_var.get().strip().lower()

        if not q:
            self.render_products()
            return

        self.render_filtered(self.load_products(), q)

    def beep(self):
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1200, 80)
        else:
            print("\a")
    
    def format_price(self, value):
        """
        Format FCFA:
        1000 -> 1 000
        105000 -> 105 000
        1000000 -> 1 000 000
        """
        try:
            return f"{int(float(value)):,}".replace(",", " ")
        except:
            return "0"

    def load_products(self):
        self.products = self.ui.product_controller.get_all_products()
        return self.products

    def render_products(self):

        # clear UI
        for w in self.products_list.winfo_children():
            w.destroy()

        # sécurité : refresh données avant rendu
        if not hasattr(self, "products") or not self.products:
            self.load_products()

        # tri stable (important pour UX POS)
        self.products.sort(key=lambda p: p.name.lower())

        # render
        for p in self.products:
            self.product_button(p)

    def render_filtered(self, products, q):
        for w in self.products_list.winfo_children():
            w.destroy()

        for p in products:
            if q not in p.name.lower() and q not in p.barcode:
                continue
            self.product_button(p)

    def product_button(self, p):
        ctk.CTkButton(
            self.products_list,
            text=f"{p.name} - {p.selling_price}",
            command=lambda pid=p.id: self.add_to_cart(pid)
        ).pack(fill="x", pady=5)

    def add_to_cart(self, product_id):
        if self.is_processing:
            return

        try:
            self.sale_service.add_product(product_id, 1)
            self.ui.event_bus.emit("sale_changed")
        except Exception as e:
            print("Add error:", e)

    def increase_qty(self, product_id):
        self.sale_service.add_product(product_id, 1)
        self.ui.event_bus.emit("sale_changed")

    def decrease_qty(self, product_id):
        try:
            self.sale_service.add_product(product_id, -1)
            self.ui.event_bus.emit("sale_changed")
        except:
            pass

    def remove_item(self, product_id):
        try:
            self.sale_service.remove_item(product_id)
            self.ui.event_bus.emit("sale_changed")
        except:
            pass

    def refresh_cart(self):

        for w in self.cart_items_frame.winfo_children():
            w.destroy()

        data = self.sale_service.get_current_sale()

        if not data or not data["items"]:
            self.total_label.configure(text="TOTAL: 0 FCFA")
            return

        total = 0

        for item in data["items"]:

            total += item["subtotal"]

            row = ctk.CTkFrame(
                self.cart_items_frame,
                corner_radius=8
            )
            row.pack(
                fill="x",
                pady=4,
                padx=2
            )

            left = ctk.CTkFrame(row, fg_color="transparent")
            left.pack(
                side="left",
                fill="both",
                expand=True,
                padx=10,
                pady=8
            )

            ctk.CTkLabel(
                left,
                text=item["product_name"],
                font=("Arial", 16, "bold"),
                anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                left,
                text=(
                    f"{item['quantity']} × "
                    f"{self.format_price(item['unit_price'])} FCFA"
                ),
                font=("Arial", 12)
            ).pack(anchor="w")

            ctk.CTkLabel(
                left,
                text=f"{self.format_price(item['subtotal'])} FCFA",
                font=("Arial", 16, "bold"),
                text_color=Theme.PRIMARY
            ).pack(anchor="w", pady=(4, 0))

            right = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )
            right.pack(
                side="right",
                padx=5,
                pady=5
            )

            ctk.CTkButton(
                right,
                text="+",
                width=35,
                command=lambda pid=item["product_id"]:
                self.increase_qty(pid)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                right,
                text="-",
                width=35,
                command=lambda pid=item["product_id"]:
                self.decrease_qty(pid)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                right,
                text="X",
                width=35,
                fg_color="#dc2626",
                command=lambda pid=item["product_id"]:
                self.remove_item(pid)
            ).pack(side="left", padx=2)

        self.total_label.configure(
            text=f"TOTAL: {self.format_price(total)} FCFA"
    )

    def start_new_sale(self):
        try:
            self.current_sale = self.sale_service.start_sale()
        except:
            pass

    def checkout(self):
        if self.is_processing:
            return

        data = self.sale_service.get_current_sale()

        if not data or not data["items"]:
            return

        self.open_cash_payment_modal()

    def cancel_sale(self):
        try:
            self.sale_service.cancel_sale()
            self.start_new_sale()
            self.ui.event_bus.emit("sale_changed")
            self.refresh_cart()
            self.scan_var.set("")
            self.focus_scan()
        except Exception as e:
            print("Cancel error:", e)

    def reprint_ticket(self):
        if not self.last_receipt:
            return

        try:
            self.sale_service.reprint_last_ticket()
        except Exception as e:
            print("Reprint error:", e)

    def show_receipt(self):

        if self.receipt_window:
            try:
                if self.receipt_window.winfo_exists():
                    self.receipt_window.focus()
                    return
            except:
                self.receipt_window = None

        if not self.last_receipt:
            return

        self.receipt_window = ctk.CTkToplevel()
        self.receipt_window.title("Receipt Preview")
        self.receipt_window.geometry("400x600")

        box = ctk.CTkTextbox(self.receipt_window)
        box.pack(fill="both", expand=True, padx=10, pady=10)

        box.insert("0.0", self.last_receipt)
        box.configure(state="disabled")

        self.receipt_window.protocol(
            "WM_DELETE_WINDOW",
            self.close_receipt_window
        )

    def close_receipt_window(self):
        if self.receipt_window:
            try:
                self.receipt_window.destroy()
            except:
                pass
        self.receipt_window = None

    def toggle_printing(self):

        enabled = self.sale_service.toggle_printing()

        if enabled:
            self.print_toggle_btn.configure(
                text="PRINT ON",
                fg_color="#16a34a"
            )
        else:
            self.print_toggle_btn.configure(
                text="PRINT OFF",
                fg_color="#dc2626"
            )
