import customtkinter as ctk

from gui.views.base_view import BaseView
from gui.cards.stat_card import StatCard
from gui.theme import Theme


class AccountingView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Accounting")

        self.ui = ui
        self.sale_service = ui.sale_service
        self.profit_window = None
        self.monthly_window = None

        self.build_ui()
        self.load_data()

        self.ui.event_bus.subscribe(
            "sale_changed",
            self.load_data
        )

        self.ui.event_bus.subscribe(
            "product_changed",
            self.load_data
        )

        self.ui.event_bus.subscribe(
            "sale_completed",
            lambda _: self.refresh_data()
        )

    # ==================================================
    # UI
    # ==================================================

    def build_ui(self):

        self.body.grid_rowconfigure(1, weight=1)
        self.body.grid_columnconfigure(0, weight=1)

        # ==========================================
        # TOP KPI
        # ==========================================

        self.kpi_frame = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )
        self.kpi_frame.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.kpi_frame.grid_columnconfigure(
            (0,1,2,3),
            weight=1
        )

        self.revenue_card = StatCard(
            self.kpi_frame,
            "TOTAL REVENUE",
            "0 FCFA",
            Theme.PRIMARY
        )
        self.revenue_card.grid(
            row=0,
            column=0,
            padx=8,
            pady=8,
            sticky="ew"
        )

        self.profit_card = StatCard(
            self.kpi_frame,
            "TOTAL PROFIT",
            "0 FCFA",
            Theme.SUCCESS
        )
        self.profit_card.grid(
            row=0,
            column=1,
            padx=8,
            pady=8,
            sticky="ew"
        )

        self.sales_card = StatCard(
            self.kpi_frame,
            "TOTAL SALES",
            "0",
            Theme.WARNING
        )
        self.sales_card.grid(
            row=0,
            column=2,
            padx=8,
            pady=8,
            sticky="ew"
        )

        self.stock_card = StatCard(
            self.kpi_frame,
            "STOCK INVESTMENT",
            "0 FCFA",
            Theme.DANGER
        )
        self.stock_card.grid(
            row=0,
            column=3,
            padx=8,
            pady=8,
            sticky="ew"
        )

        # ==========================================
        # CENTER
        # ==========================================

        self.center = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )
        self.center.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.center.grid_columnconfigure(
            0,
            weight=55
        )

        self.center.grid_columnconfigure(
            1,
            weight=45
        )

        self.center.grid_rowconfigure(
            0,
            weight=1
        )

        # ==========================================
        # LEFT PANEL
        # ==========================================

        self.report_frame = ctk.CTkFrame(
            self.center,
            corner_radius=12
        )
        self.report_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,5)
        )

        ctk.CTkLabel(
            self.report_frame,
            text="BUSINESS REPORTS",
            font=("Arial",18,"bold"),
            text_color=Theme.PRIMARY
        ).pack(
            anchor="w",
            padx=20,
            pady=15
        )

        self.period_buttons = ctk.CTkFrame(
            self.report_frame,
            fg_color="transparent"
        )
        self.period_buttons.pack(
            fill="x",
            padx=15
        )

        periods = [
            ("TODAY", self.load_today),
            ("WEEK", self.load_week),
            ("MONTH", self.load_month),
            ("REPORTS", self.show_monthly_reports)
        ]

        for text, cmd in periods:

            ctk.CTkButton(
                self.period_buttons,
                text=text,
                command=cmd,
                width=100
            ).pack(
                side="left",
                padx=5
            )

        self.report_content = ctk.CTkScrollableFrame(
            self.report_frame
        )
        self.report_content.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # RIGHT PANEL
        # ==========================================

        self.analytics = ctk.CTkFrame(
            self.center,
            corner_radius=12
        )
        self.analytics.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5,0)
        )

        ctk.CTkLabel(
            self.analytics,
            text="BUSINESS ANALYTICS",
            font=("Arial",18,"bold"),
            text_color=Theme.PRIMARY
        ).pack(
            anchor="w",
            padx=20,
            pady=15
        )

        self.analytics_scroll = ctk.CTkScrollableFrame(
            self.analytics
        )
        self.analytics_scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.profit_btn = ctk.CTkButton(
            self.analytics,
            text="VIEW FULL PROFIT RANKING",
            command=self.show_profit_ranking
        )

        self.profit_btn.pack(
            fill="x",
            padx=15,
            pady=10
        )

    # ==================================================
    # HELPERS
    # ==================================================

    def money(self, value):

        return (
            f"{int(value):,}"
            .replace(",", " ")
            + " FCFA"
        )

    # ==================================================
    # LOAD GLOBAL DATA
    # ==================================================

    def load_data(self, _=None):

        report = self.sale_service.get_profit_report()

        stock = self.sale_service.get_stock_valuation()

        sales = self.sale_service.get_sales_count(
            self.sale_service.get_sales_history()
        )

        self.revenue_card.update_value(
            self.money(
                report["revenue"]
            )
        )

        self.profit_card.update_value(
            self.money(
                report["profit"]
            )
        )

        self.sales_card.update_value(
            str(sales)
        )

        self.stock_card.update_value(
            self.money(
                stock["total_value"]
            )
        )

        self.load_today()
        self.load_analytics()

    # ==================================================
    # REPORT DISPLAY
    # ==================================================

    def display_report(self, sales):

        for w in self.report_content.winfo_children():
            w.destroy()

        profit = self.sale_service.get_profit_for_sales(
            sales
        )

        stats = [

            ("Revenue",
             self.money(
                 profit["revenue"])),

            ("Cost",
             self.money(
                 profit["cost"])),

            ("Profit",
             self.money(
                 profit["profit"])),

            ("Transactions",
             str(len(sales))),

            ("Average Ticket",
             self.money(
                 self.sale_service.get_average_ticket(
                     sales
                 ))),

            ("Margin",
             f"{self.sale_service.get_profit_margin(sales)} %")
        ]

        for title, value in stats:

            box = ctk.CTkFrame(
                self.report_content
            )

            box.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                box,
                text=title,
                font=("Arial",14)
            ).pack(
                anchor="w",
                padx=15,
                pady=(10,0)
            )

            ctk.CTkLabel(
                box,
                text=value,
                font=("Arial",18,"bold")
            ).pack(
                anchor="w",
                padx=15,
                pady=(0,10)
            )

    # ==================================================
    # ANALYTICS
    # ==================================================

    def load_analytics(self):

        for w in self.analytics_scroll.winfo_children():
            w.destroy()

        best = self.sale_service.get_top_selling_products(5)

        ctk.CTkLabel(
            self.analytics_scroll,
            text="TOP 5 BEST SELLERS",
            font=("Arial",16,"bold")
        ).pack(
            anchor="w",
            pady=5
        )

        for p in best:

            ctk.CTkLabel(
                self.analytics_scroll,
                text=(
                    f"{p['name']} "
                    f"({p['quantity_sold']})"
                )
            ).pack(
                anchor="w",
                padx=10
            )

        ctk.CTkLabel(
            self.analytics_scroll,
            text="",
            height=15
        ).pack()

        stock = self.sale_service.get_stock_valuation()

        ctk.CTkLabel(
            self.analytics_scroll,
            text="STOCK VALUE",
            font=("Arial",16,"bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.analytics_scroll,
            text=self.money(
                stock["total_value"]
            )
        ).pack(anchor="w")

    # ==================================================
    # PERIODS
    # ==================================================

    def load_today(self):
        self.display_report(
            self.sale_service.get_today_sales()
        )

    def load_week(self):
        self.display_report(
            self.sale_service.get_week_sales()
        )

    def load_month(self):
        self.display_report(
            self.sale_service.get_month_sales()
        )

    def load_all(self):
        self.display_report(
            self.sale_service.get_sales_history()
        )

    # ==================================================
    # PROFIT RANKING
    # ==================================================

    def show_profit_ranking(self):

        if (
            self.profit_window
            and self.profit_window.winfo_exists()
        ):
            self.profit_window.focus()
            return

        self.profit_window = ctk.CTkToplevel(self)

        self.profit_window.title(
            "Profit Ranking"
        )

        self.profit_window.geometry(
            "700x600"
        )

        scroll = ctk.CTkScrollableFrame(
            self.profit_window
        )

        scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        ranking = (
            self.sale_service
            .get_product_profit_ranking()
        )

        for i, p in enumerate(
            ranking,
            1
        ):

            ctk.CTkLabel(
                scroll,
                text=(
                    f"{i}. "
                    f"{p['name']}    "
                    f"Profit: "
                    f"{self.money(p['total_profit'])}"
                ),
                font=("Arial",15)
            ).pack(
                anchor="w",
                pady=5
            )

        self.profit_window.protocol(
            "WM_DELETE_WINDOW",
            self.close_profit_window
        )

    def show_monthly_reports(self):

        if (
            self.monthly_window
            and self.monthly_window.winfo_exists()
        ):
            self.monthly_window.focus()
            return

        self.monthly_window = ctk.CTkToplevel(self)

        self.monthly_window.title(
            "Monthly Reports"
        )

        self.monthly_window.geometry(
            "1000x650"
        )

        self.monthly_window.grid_columnconfigure(
            0,
            weight=1
        )

        self.monthly_window.grid_columnconfigure(
            1,
            weight=3
        )

        self.monthly_window.grid_rowconfigure(
            0,
            weight=1
        )

        # =================================
        # MONTH LIST
        # =================================

        left = ctk.CTkScrollableFrame(
            self.monthly_window,
            width=220
        )

        left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        # =================================
        # REPORT
        # =================================

        self.month_report = ctk.CTkScrollableFrame(
            self.monthly_window
        )

        self.month_report.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        sales = self.sale_service.get_sales_history()

        months = {}

        for sale in sales:

            month = sale["created_at"][:7]

            if month not in months:
                months[month] = []

            months[month].append(sale)

        for month in sorted(
            months.keys(),
            reverse=True
        ):

            ctk.CTkButton(
                left,
                text=month,
                command=lambda
                    m=month,
                    s=months[month]:
                        self.load_month_report(
                            m,
                            s
                        )
            ).pack(
                fill="x",
                pady=3
            )

        self.monthly_window.protocol(
            "WM_DELETE_WINDOW",
            self.close_monthly_window
        )

    def close_profit_window(self):

        if self.profit_window:
            self.profit_window.destroy()

        self.profit_window = None


    def close_monthly_window(self):

        if self.monthly_window:
            self.monthly_window.destroy()

        self.monthly_window = None

    def load_month_report(
            self,
            month,
            sales
    ):

        for w in self.month_report.winfo_children():
            w.destroy()

        profit = (
            self.sale_service
            .get_profit_for_sales(
                sales
            )
        )

        avg = (
            self.sale_service
            .get_average_ticket(
                sales
            )
        )

        margin = (
            self.sale_service
            .get_profit_margin(
                sales
            )
        )

        top = (
            self.sale_service
            .get_top_selling_products(
                1
            )
        )

        unsold = (
            self.sale_service
            .get_unsold_products()
        )

        title = ctk.CTkLabel(
            self.month_report,
            text=f"REPORT {month}",
            font=("Arial",22,"bold"),
            text_color=Theme.PRIMARY
        )

        title.pack(
            anchor="w",
            pady=10
        )

        stats = [

            (
                "Revenue",
                self.money(
                    profit["revenue"]
                )
            ),

            (
                "Cost",
                self.money(
                    profit["cost"]
                )
            ),

            (
                "Profit",
                self.money(
                    profit["profit"]
                )
            ),

            (
                "Transactions",
                str(len(sales))
            ),

            (
                "Average Ticket",
                self.money(avg)
            ),

            (
                "Margin",
                f"{margin}%"
            ),

            (
                "Best Seller",
                top[0]["name"]
                if top
                else "-"
            ),

            (
                "Units Sold",
                str(
                    top[0]["quantity_sold"]
                )
                if top
                else "0"
            ),

            (
                "Unsold Products",
                str(len(unsold))
            )
        ]

        for label, value in stats:

            card = ctk.CTkFrame(
                self.month_report
            )

            card.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                card,
                text=label,
                font=("Arial",14)
            ).pack(
                anchor="w",
                padx=15,
                pady=(10,0)
            )

            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial",18,"bold")
            ).pack(
                anchor="w",
                padx=15,
                pady=(0,10)
            )
