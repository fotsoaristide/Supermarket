import customtkinter as ctk
from gui.views.base_view import BaseView
from gui.cards.stat_card import StatCard
from gui.theme import Theme


class DashboardView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Dashboard")

        self.ui = ui

        self.build_dashboard()
        self.load_data()
        self.ui.event_bus.subscribe("product_changed", self.load_data)

    # =========================
    # UI BUILD
    # =========================
    def build_dashboard(self):

        self.stats_frame = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )
        self.stats_frame.grid(row=0, column=0, sticky="ew")

        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # =========================
        # CARDS (VIDES AU DÉPART)
        # =========================

        self.sales_card = StatCard(
            self.stats_frame,
            "Ventes Aujourd'hui",
            "0 FCFA",
            Theme.SUCCESS
        )
        self.sales_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.products_card = StatCard(
            self.stats_frame,
            "Produits",
            "0",
            Theme.PRIMARY
        )
        self.products_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.stock_card = StatCard(
            self.stats_frame,
            "Stock Total",
            "0",
            Theme.WARNING
        )
        self.stock_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.revenue_card = StatCard(
            self.stats_frame,
            "Bénéfice Aujourd'hui",
            "0 FCFA",
            Theme.DANGER
        )
        self.revenue_card.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # =========================
        # ZONE BASSE
        # =========================

        self.bottom_frame = ctk.CTkFrame(
            self.body,
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS
        )
        self.bottom_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.body.grid_rowconfigure(1, weight=1)

        label = ctk.CTkLabel(
            self.bottom_frame,
            text="Dashboard connecté au backend",
            font=Theme.TEXT_FONT,
            text_color=Theme.TEXT_LIGHT
        )
        label.pack(pady=40)

    # =========================
    # BACKEND LOADING
    # =========================
    def load_data(self, _=None):

        try:
            products = self.ui.product_controller.get_all_products()
            product_count = len(products)

            total_stock = sum(p.quantity for p in products)

            today_revenue = self.ui.sale_service.get_today_total()
            profit_data = self.ui.sale_service.get_today_profit_report()
            today_profit = profit_data["profit"]

            self.products_card.update_value(str(product_count))
            self.stock_card.update_value(str(total_stock))
            self.revenue_card.update_value(f"{today_profit} FCFA")
            self.sales_card.update_value(f"{today_revenue} FCFA")

        except Exception as e:
            print("Dashboard load error:", e)
