import customtkinter as ctk
from gui.views.base_view import BaseView
from gui.cards.stat_card import StatCard
from gui.theme import Theme


class AccountingView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Accounting")

        self.ui = ui

        self.build_ui()

    def build_ui(self):

        # =========================
        # KPI SECTION
        # =========================

        self.kpi_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.kpi_frame.grid(row=0, column=0, sticky="ew")

        self.kpi_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # =========================
        # KPI CARDS (mock data)
        # =========================

        self.revenue_card = StatCard(
            self.kpi_frame,
            "Chiffre d'affaires",
            "120 000 FCFA",
            Theme.PRIMARY
        )
        self.revenue_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.profit_card = StatCard(
            self.kpi_frame,
            "Bénéfice",
            "45 000 FCFA",
            Theme.SUCCESS
        )
        self.profit_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.transactions_card = StatCard(
            self.kpi_frame,
            "Transactions",
            "24",
            Theme.WARNING
        )
        self.transactions_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.avg_cart_card = StatCard(
            self.kpi_frame,
            "Panier moyen",
            "5 000 FCFA",
            Theme.DANGER
        )
        self.avg_cart_card.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # =========================
        # ZONE GRAPHIQUE (placeholder)
        # =========================

        self.graph_frame = ctk.CTkFrame(
            self.body,
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS
        )
        self.graph_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.body.grid_rowconfigure(1, weight=1)

        label = ctk.CTkLabel(
            self.graph_frame,
            text="Analytics chart area (backend integration later)",
            font=Theme.TEXT_FONT,
            text_color=Theme.TEXT_LIGHT
        )
        label.pack(pady=40)
