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
        self.ui.event_bus.subscribe(
            "product_changed",
            self.load_data
        )

        self.ui.event_bus.subscribe(
            "sale_changed",
            self.load_data
        )

        self.ui.event_bus.subscribe(
            "sale_completed",
            lambda _: self.refresh_dashboard()
        )
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
            "Today's Sales",
            "0 FCFA",
            Theme.DANGER
        )

        self.products_card = StatCard(
            self.stats_frame,
            "Products",
            "0",
            Theme.PRIMARY
        )

        self.stock_card = StatCard(
            self.stats_frame,
            "Total Stock",
            "0",
            Theme.WARNING
        )

        self.revenue_card = StatCard(
            self.stats_frame,
            "Today's Profit",
            "0 FCFA",
            Theme.SUCCESS
        )
        self.revenue_card.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        self.sales_card.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.products_card.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.stock_card.grid(
            row=0,
            column=2,
            padx=10,
            pady=10,
            sticky="ew"
        )
        
        # =========================
        # BOTTOM AREA
        # =========================

        self.bottom_frame = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )
        self.bottom_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.body.grid_rowconfigure(1, weight=1)

        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)

        # ==================================
        # LOW STOCK ALERTS
        # ==================================

        self.low_stock_frame = ctk.CTkFrame(
            self.bottom_frame,
            corner_radius=12
        )
        self.low_stock_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5)
        )

        ctk.CTkLabel(
            self.low_stock_frame,
            text="⚠ LOW STOCK ALERTS",
            font=("Arial", 17, "bold"),
            text_color="#dc2626"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

        self.low_stock_list = ctk.CTkScrollableFrame(
            self.low_stock_frame
        )
        self.low_stock_list.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # ==================================
        # PRODUCT STATISTICS
        # ==================================

        self.product_stats_frame = ctk.CTkFrame(
            self.bottom_frame,
            corner_radius=12
        )
        self.product_stats_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0)
        )

        ctk.CTkLabel(
            self.product_stats_frame,
            text="PRODUCT STATISTICS",
            font=("Arial", 17, "bold"),
            text_color=Theme.PRIMARY
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

        self.product_stats_content = ctk.CTkFrame(
            self.product_stats_frame,
            fg_color="transparent"
        )
        self.product_stats_content.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0,10)
        )

        self.product_stats_content.grid_columnconfigure(
            0,
            weight=1
        )

        self.product_stats_content.grid_columnconfigure(
            1,
            weight=1
        )
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

            # ==================================
            # LOW STOCK PANEL
            # ==================================

            for w in self.low_stock_list.winfo_children():
                w.destroy()

            alerts = [
                p
                for p in products
                if p.quantity <= p.minimum_stock
            ]

            if not alerts:

                ctk.CTkLabel(
                    self.low_stock_list,
                    text="No stock alerts",
                    font=("Arial", 14)
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=10
                )

            else:

                for p in alerts[:15]:

                    ctk.CTkLabel(
                        self.low_stock_list,
                        text=(
                            f"{p.name}    "
                            f"({p.quantity}/{p.minimum_stock})"
                        ),
                        font=("Arial", 15, "bold"),
                        text_color="black",
                        anchor="w"
                    ).pack(
                        fill="x",
                        padx=15,
                        pady=6
                    )
            
            # ==================================
            # PRODUCT STATISTICS
            # ==================================

            for w in self.product_stats_content.winfo_children():
                w.destroy()

            inventory_value = sum(
                p.quantity * p.purchase_price
                for p in products
            )

            potential_profit = sum(
                p.quantity * p.profit
                for p in products
            )

            best_profit = sorted(
                products,
                key=lambda p: p.profit,
                reverse=True
            )[:5]

            # ==================================
            # INVENTORY VALUE
            # ==================================

            card = ctk.CTkFrame(
                self.product_stats_content,
                corner_radius=8
            )

            card.grid(
                row=0,
                column=0,
                sticky="nsew",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                card,
                text="Inventory Value",
                font=("Arial", 14, "bold"),
                text_color=Theme.PRIMARY
            ).pack(
                anchor="w",
                padx=10,
                pady=(8,0)
            )

            ctk.CTkLabel(
                card,
                text=f"{int(inventory_value):,} FCFA",
                font=("Arial",16,"bold")
            ).pack(
                anchor="w",
                padx=10,
                pady=(0,8)
            )

            # ==================================
            # POTENTIAL PROFIT
            # ==================================

            card = ctk.CTkFrame(
                self.product_stats_content,
                corner_radius=8
            )

            card.grid(
                row=0,
                column=1,
                sticky="nsew",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                card,
                text="Potential Profit",
                font=("Arial",14,"bold"),
                text_color=Theme.SUCCESS
            ).pack(
                anchor="w",
                padx=10,
                pady=(8,0)
            )

            ctk.CTkLabel(
                card,
                text=f"{int(potential_profit):,} FCFA",
                font=("Arial",16,"bold")
            ).pack(
                anchor="w",
                padx=10,
                pady=(0,8)
            )

            # ==================================
            # TOP 5 PRODUCTS
            # ==================================

            card = ctk.CTkFrame(
                self.product_stats_content,
                corner_radius=8
            )

            card.grid(
                row=1,
                column=0,
                sticky="nsew",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                card,
                text="TOP 5 PRODUCTS",
                font=("Arial",14,"bold"),
                text_color=Theme.PRIMARY
            ).pack(
                anchor="w",
                padx=10,
                pady=8
            )

            for p in products[:5]:

                ctk.CTkLabel(
                    card,
                    text=f"• {p.name}",
                    font=("Arial",13),
                    text_color="black"
                ).pack(
                    anchor="w",
                    padx=20
                )

            # ==================================
            # MOST PROFITABLE
            # ==================================

            card = ctk.CTkFrame(
                self.product_stats_content,
                corner_radius=8
            )

            card.grid(
                row=1,
                column=1,
                sticky="nsew",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                card,
                text="MOST PROFITABLE",
                font=("Arial",14,"bold"),
                text_color=Theme.SUCCESS
            ).pack(
                anchor="w",
                padx=10,
                pady=8
            )

            for p in best_profit:

                ctk.CTkLabel(
                    card,
                    text=(
                        f"• {p.name} "
                        f"(+{int(p.profit):,})"
                    ),
                    font=("Arial",13),
                    text_color="black"
                ).pack(
                    anchor="w",
                    padx=20
                )

            # ==================================
            # PRODUCTS REGISTERED
            # ==================================

            card = ctk.CTkFrame(
                self.product_stats_content,
                corner_radius=8
            )

            card.grid(
                row=2,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                card,
                text="Products Registered",
                font=("Arial",14,"bold"),
                text_color=Theme.PRIMARY
            ).pack(
                anchor="w",
                padx=10,
                pady=(8,0)
            )

            ctk.CTkLabel(
                card,
                text=str(product_count),
                font=("Arial",16,"bold")
            ).pack(
                anchor="w",
                padx=10,
                pady=(0,8)
            )

            self.products_card.update_value(str(product_count))
            self.stock_card.update_value(str(total_stock))
            self.revenue_card.update_value(f"{today_profit} FCFA")
            self.sales_card.update_value(f"{today_revenue} FCFA")

        except Exception as e:
            print("Dashboard load error:", e)
