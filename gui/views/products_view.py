import customtkinter as ctk
from gui.views.base_view import BaseView
from gui.theme import Theme
from gui.dialogs.product_dialog import ProductDialog


class ProductsView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Products")

        self.ui = ui
        self.products = []
        self.filtered_products = []
        self.selected_product = None

        self.build_ui()
        self.load_products()
        self.render_products()

        self.ui.event_bus.subscribe("product_changed", self.refresh)

    # =========================
    # UI LAYOUT (POS PRO SPLIT)
    # =========================
    def build_ui(self):

        # 2 colonnes asymétriques POS
        self.body.grid_columnconfigure(0, weight=4)
        self.body.grid_columnconfigure(1, weight=3)
        self.body.grid_rowconfigure(0, weight=1)

        # =========================
        # LEFT PANEL WRAPPER
        # =========================
        self.left_panel = ctk.CTkFrame(self.body)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.left_panel.grid_rowconfigure(2, weight=1)
        self.left_panel.grid_columnconfigure(0, weight=1)

        # =========================
        # TOP BAR (SEARCH + ADD)
        # =========================
        top = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", pady=(10, 5))

        top.grid_columnconfigure(0, weight=1)

        self.search = ctk.CTkEntry(
            top,
            placeholder_text="Search product..."
        )
        self.search.grid(row=0, column=0, sticky="ew", padx=(10, 10))
        self.search.bind("<KeyRelease>", lambda e: self.filter_products())

        self.add_btn = ctk.CTkButton(
            top,
            text="Add Product",
            fg_color=Theme.PRIMARY,
            command=self.open_add_dialog
        )
        self.add_btn.grid(row=0, column=1, padx=(0, 10))

        # =========================
        # DASHBOARD CARDS
        # =========================
        self.stats_frame = ctk.CTkFrame(
            self.body,
            corner_radius=10
        )
        self.stats_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 10)
        )

        # =========================
        # STATS CARDS
        # =========================

        self.stats_frame.grid_columnconfigure((0,1,2), weight=1)

        self.products_card = ctk.CTkFrame(
            self.stats_frame,
            corner_radius=10
        )
        self.products_card.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            self.products_card,
            text="PRODUCTS",
            font=("Arial",12,"bold"),
            text_color=Theme.PRIMARY
        ).pack(pady=(8,0))

        self.total_products_label = ctk.CTkLabel(
            self.products_card,
            text="0",
            font=("Arial",22,"bold")
        )
        self.total_products_label.pack(pady=(0,8))


        self.low_card = ctk.CTkFrame(
            self.stats_frame,
            corner_radius=10
        )
        self.low_card.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            self.low_card,
            text="LOW",
            font=("Arial",12,"bold"),
            text_color="#dc2626"
        ).pack(pady=(8,0))

        self.low_stock_label = ctk.CTkLabel(
            self.low_card,
            text="0",
            font=("Arial",22,"bold")
        )
        self.low_stock_label.pack(pady=(0,8))


        self.stock_card = ctk.CTkFrame(
            self.stats_frame,
            corner_radius=10
        )
        self.stock_card.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            self.stock_card,
            text="STOCK",
            font=("Arial",12,"bold"),
            text_color=Theme.PRIMARY
        ).pack(pady=(8,0))

        self.stock_value_label = ctk.CTkLabel(
            self.stock_card,
            text="0",
            font=("Arial",22,"bold")
        )
        self.stock_value_label.pack(pady=(0,8))

        self.alert_frame = ctk.CTkFrame(
            self.body,
            corner_radius=10
        )
        self.alert_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0,10)
        )

        self.alert_label = ctk.CTkLabel(
            self.alert_frame,
            text="No alerts",
            anchor="w"
        )
        self.alert_label.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # =========================
        # MINI DASHBOARD (TOP / LOW / ALERTS)
        # =========================
        self.dashboard = ctk.CTkFrame(self.left_panel, height=110)
        self.dashboard.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.dashboard_label = ctk.CTkLabel(
            self.dashboard,
            text="Top Products | Low Stock | Out of Stock Alerts",
            font=("Arial", 13, "bold"),
            text_color=Theme.PRIMARY
        )
        self.dashboard_label.pack(pady=20)

        # =========================
        # PRODUCT LIST (CLEAN LIST STYLE)
        # =========================
        self.list_frame = ctk.CTkScrollableFrame(self.left_panel)
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # =========================
        # RIGHT PANEL (DETAIL / EDIT)
        # =========================
        self.detail_panel = ctk.CTkFrame(self.body, corner_radius=12)
        self.detail_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.detail_panel.grid_rowconfigure(1, weight=1)
        self.detail_panel.grid_columnconfigure(0, weight=1)

        # TITLE
        self.detail_title = ctk.CTkLabel(
            self.detail_panel,
            text="PRODUCT DETAILS / EDIT",
            font=("Arial", 18, "bold"),
            text_color=Theme.PRIMARY
        )
        self.detail_title.pack(pady=10)

       # CONTENT AREA (FIXED ERP STYLE)
        self.detail_content = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        self.detail_content.pack(fill="both", expand=True, padx=15, pady=10)

        # HEADER
        self.detail_header = ctk.CTkLabel(
            self.detail_content,
            text="Select a product",
            font=("Arial", 16, "bold"),
            anchor="w"
        )
        self.detail_header.pack(fill="x", pady=(0, 10))

        # BODY GRID (2 columns ERP STYLE)
        self.detail_body = ctk.CTkFrame(self.detail_content, fg_color="transparent")
        self.detail_body.pack(fill="both", expand=True)

        self.detail_body.grid_columnconfigure(0, weight=1)
        self.detail_body.grid_columnconfigure(1, weight=1)

        # LEFT COLUMN
        self.left_info = ctk.CTkFrame(self.detail_body, fg_color="transparent")
        self.left_info.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # RIGHT COLUMN
        self.right_info = ctk.CTkFrame(self.detail_body, fg_color="transparent")
        self.right_info.grid(row=0, column=1, sticky="nsew")

        # =========================
        # ACTIONS (BOTTOM RIGHT)
        # =========================
        self.action_frame = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=15, pady=15)

        self.update_btn = ctk.CTkButton(
            self.action_frame,
            text="UPDATE",
            fg_color=Theme.PRIMARY,
            height=45,
            command=self.open_update
        )
        self.update_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.delete_btn = ctk.CTkButton(
            self.action_frame,
            text="DELETE",
            fg_color="#dc2626",
            height=45,
            command=self.delete_selected
        )
        self.delete_btn.pack(side="left", expand=True, fill="x", padx=5)

    # =========================
    # FORMAT PRICE
    # =========================
    def format_price(self, value):
        try:
            return f"{int(float(value)):,}".replace(",", " ")
        except:
            return "0"
        
    # =========================
    # CONFIRMATION DIALOG
    # =========================
    def confirm_action(self, title, message):

        dialog = ctk.CTkToplevel(self)

        dialog.title(title)
        dialog.geometry("350x170")
        dialog.resizable(False, False)
        dialog.grab_set()

        result = {"value": False}

        ctk.CTkLabel(
            dialog,
            text=message,
            justify="center",
            font=("Arial", 14)
        ).pack(
            expand=True,
            pady=20,
            padx=20
        )

        button_frame = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )
        button_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        def yes():
            result["value"] = True
            dialog.destroy()

        def no():
            dialog.destroy()

        ctk.CTkButton(
            button_frame,
            text="YES",
            fg_color="#16a34a",
            command=yes
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="NO",
            fg_color="#dc2626",
            command=no
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        dialog.wait_window()

        return result["value"]

    # =========================
    # LOAD BACKEND (UNCHANGED)
    # =========================
    def load_products(self):

        try:
            raw = self.ui.product_controller.get_all_products()

            self.products = [
                {
                    "id": p.id,
                    "barcode": p.barcode,
                    "name": p.name,
                    "category": p.category,

                    "purchase_price": p.purchase_price,
                    "price": p.selling_price,

                    "stock": p.quantity,
                    "minimum_stock": p.minimum_stock,

                    "profit": p.profit,
                    "low_stock": p.is_low_stock,

                    "created_at": p.created_at,
                    "updated_at": p.updated_at
                }
                for p in raw
            ]

            self.filtered_products = self.products

        except Exception as e:
            print("Products load error:", e)
            self.products = []
            self.filtered_products = []
    
    # =========================
    # STATISTICS
    # =========================
    def refresh_statistics(self):

        total_products = len(self.products)

        low_stock = sum(
            1
            for p in self.products
            if p["low_stock"]
        )

        total_stock = sum(
            p["stock"]
            for p in self.products
        )

        self.total_products_label.configure(
            text=f"{total_products}"
        )

        self.low_stock_label.configure(
            text=f"{low_stock}"
        )

        self.stock_value_label.configure(
            text=f"{total_stock}"
        )

    # =========================
    # FILTER
    # =========================
    def filter_products(self):

        q = self.search.get().lower().strip()

        if not q:
            self.filtered_products = self.products
        else:
            self.filtered_products = [
                p for p in self.products
                if q in p["name"].lower()
                or q in p["barcode"].lower()
            ]

        self.render_products()

    # =========================
    # SELECT PRODUCT (SIMPLE CLICK)
    # =========================
    def select_product(self, product):

        self.selected_product = product

        stock_state = "LOW STOCK" if product["low_stock"] else "AVAILABLE"

        # HEADER
        self.detail_header.configure(
            text=product["name"]
        )

        # CLEAR OLD CONTENT
        for w in self.left_info.winfo_children():
            w.destroy()

        for w in self.right_info.winfo_children():
            w.destroy()

        # =========================
        # LEFT COLUMN (IDENTITY)
        # =========================
        ctk.CTkLabel(
            self.left_info,
            text="IDENTITY",
            font=("Arial", 14, "bold"),
            text_color=Theme.PRIMARY
        ).pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(
            self.left_info,
            text=f"Barcode: {product['barcode']}",
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.left_info,
            text=f"Category: {product['category']}",
            anchor="w"
        ).pack(anchor="w")

        # =========================
        # RIGHT COLUMN (FINANCE + STOCK)
        # =========================
        ctk.CTkLabel(
            self.right_info,
            text="FINANCE",
            font=("Arial", 14, "bold"),
            text_color=Theme.PRIMARY
        ).pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(
            self.right_info,
            text=f"Purchase: {self.format_price(product['purchase_price'])}",
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.right_info,
            text=f"Selling: {self.format_price(product['price'])}",
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.right_info,
            text=f"Profit: {self.format_price(product['profit'])}",
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.right_info,
            text="\nSTOCK",
            font=("Arial", 14, "bold"),
            text_color=Theme.PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.right_info,
            text=f"Qty: {product['stock']}",
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.right_info,
            text=f"Min: {product['minimum_stock']}",
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.right_info,
            text=f"Status: {stock_state}",
            text_color=("#dc2626" if product["low_stock"] else "#16a34a")
        ).pack(anchor="w")

        # =========================
        # FIXED ACTION STATE SAFE
        # =========================
        self.update_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")

        self.render_products()

    # =========================
    # UPDATE
    # =========================
    def open_update(self):

        if not self.selected_product:
            return

        ProductDialog(
            self,
            self.ui,
            product=self.selected_product,
            edit_mode=True
        )

    # =========================
    # DELETE
    # =========================
    def delete_selected(self):

        if not self.selected_product:
            return

        confirmed = self.confirm_action(
            "Confirm Delete",
            f"Delete product\n\n"
            f"{self.selected_product['name']} ?"
        )

        if not confirmed:
            return

        try:

            self.ui.product_controller.delete_product_by_id(
                self.selected_product["id"]
            )

            self.selected_product = None

            self.refresh()

        except Exception as e:
            print("Delete error:", e)

    # =========================
    # RENDER PRODUCTS
    # =========================
    def render_products(self):

        for w in self.list_frame.winfo_children():
            w.destroy()

        for product in self.filtered_products:

            is_selected = (
                self.selected_product
                and
                product["id"] == self.selected_product["id"]
            )

            default_color = (
                Theme.PRIMARY
                if is_selected
                else "#2b2b2b"
            )

            row = ctk.CTkFrame(
                self.list_frame,
                height=42,
                corner_radius=18,
                fg_color=default_color
            )

            row.pack(
                fill="x",
                padx=5,
                pady=3
            )

            row.pack_propagate(False)

            def enter(event, frame=row, selected=is_selected):
                if not selected:
                    frame.configure(
                        fg_color="#404040"
                    )

            def leave(event, frame=row, selected=is_selected):
                if not selected:
                    frame.configure(
                        fg_color="#2b2b2b"
                    )

            row.bind("<Enter>", enter)
            row.bind("<Leave>", leave)

            name = product["name"]

            if product["low_stock"]:
                name += " ⚠"

            ctk.CTkLabel(
                row,
                text=name,
                font=("Arial",13),
                anchor="w"
            ).pack(
                side="left",
                padx=15
            )

            ctk.CTkLabel(
                row,
                text=str(product["stock"]),
                width=50
            ).pack(
                side="right",
                padx=10
            )

            ctk.CTkLabel(
                row,
                text=f"{self.format_price(product['price'])}",
                text_color=Theme.PRIMARY,
                width=80
            ).pack(
                side="right",
                padx=10
            )

            row.bind(
                "<Button-1>",
                lambda e, p=product:
                self.select_product(p)
            )

    def open_add_dialog(self):
        ProductDialog(self, self.ui)
        
    # =========================
    # ALERTS
    # =========================
    def refresh_alerts(self):

        alerts = [
            p
            for p in self.products
            if p["low_stock"]
        ]

        if not alerts:

            self.alert_label.configure(
                text="No stock alerts"
            )
            return

        txt = []

        for p in alerts[:3]:

            txt.append(
                f"⚠ {p['name']} "
                f"({p['stock']}/{p['minimum_stock']})"
            )

        self.alert_label.configure(
            text="\n".join(txt)
        )

    # =========================
    # REFRESH
    # =========================
    def refresh(self, data=None):

        self.load_products()

        self.refresh_statistics()

        self.refresh_alerts()

        self.render_products()