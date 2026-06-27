import customtkinter as ctk
from gui.views.base_view import BaseView
from gui.theme import Theme
from utils.formatter import Formatter


class HistoryView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "History")

        self.ui = ui
        self.sale_service = ui.sale_service

        self.selected_sale_id = None
        self.selected_row = None

        self.build_ui()

        self.load_sales()

        # Rafraîchit automatiquement après chaque vente
        self.ui.event_bus.subscribe(
            "sale_completed",
            lambda _: self.load_sales()
        )
    # =========================
    # UI
    # =========================
    def build_ui(self):

        self.body.grid_rowconfigure(1, weight=1)
        self.body.grid_columnconfigure(0, weight=1)

        # =========================
        # TOP BAR
        # =========================

        top_bar = ctk.CTkFrame(self.body, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        top_bar.grid_columnconfigure(0, weight=1)

        self.search = ctk.CTkEntry(
            top_bar,
            placeholder_text="Search sale ID..."
        )
        self.search.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search.bind("<KeyRelease>", lambda e: self.load_sales())

        self.filter = ctk.CTkOptionMenu(
            top_bar,
            values=["All", "Completed"],
            command=lambda _: self.load_sales()
        )
        self.filter.grid(row=0, column=1)

        # =========================
        # MAIN AREA
        # =========================

        self.main = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )

        self.main.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=5
        )

        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=2)
        self.main.grid_columnconfigure(1, weight=3)

        # =========================
        # LEFT : SALES LIST
        # =========================

        self.table_frame = ctk.CTkScrollableFrame(self.main)

        self.table_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        # =========================
        # RIGHT : TICKET PREVIEW
        # =========================

        self.details = ctk.CTkFrame(
            self.main,
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS
        )

        self.details.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.details_text = ctk.CTkTextbox(
            self.details,
            font=("Courier New", 13)
        )

        self.details_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.details_text.configure(state="disabled")

        # =========================
        # FOOTER
        # =========================

        footer = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )

        footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        self.reprint_btn = ctk.CTkButton(
            footer,
            text="Reprint",
            fg_color=Theme.PRIMARY,
            command=self.reprint_selected
        )

        self.reprint_btn.pack(side="right")

    def load_sales(self):

        from datetime import datetime

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        search = self.search.get().strip()
        filter_value = self.filter.get()

        sales = self.sale_service.get_sales_history()

        if search:
            sales = [
                sale for sale in sales
                if search in str(sale["id"])
            ]

        if filter_value == "Completed":
            sales = [
                sale for sale in sales
                if sale["status"] == "COMPLETED"
            ]

        # ==========================
        # HEADER
        # ==========================

        header = ctk.CTkFrame(
            self.table_frame,
            fg_color="#ECECEC",
            corner_radius=6
        )

        header.pack(fill="x", pady=(0, 6))

        headers = [
            ("ID", 70),
            ("DATE", 150),
            ("HEURE", 90),
            ("TOTAL", 120),
            ("STATUS", 100)
        ]

        for text, width in headers:

            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                font=Theme.TEXT_FONT,
                text_color=Theme.TEXT
            ).pack(side="left", padx=5, pady=6)

        # ==========================
        # ROWS
        # ==========================

        for index, sale in enumerate(sales):

            try:
                dt = datetime.fromisoformat(
                    sale["created_at"]
                )

                date = dt.strftime("%d/%m/%Y")
                hour = dt.strftime("%H:%M")

            except Exception:
                date = sale["created_at"]
                hour = ""

            bg = "#FFFFFF" if index % 2 == 0 else "#F7F7F7"

            row = ctk.CTkFrame(
                self.table_frame,
                fg_color=bg,
                corner_radius=6
            )

            row.pack(fill="x", pady=2)

            widgets = [

                (f"#{sale['id']}", 70),

                (date, 150),

                (hour, 90),

                (f"{sale['total']} FCFA", 120),

                ("✓ Payée", 100)

            ]

            for text, width in widgets:

                label = ctk.CTkLabel(
                    row,
                    text=text,
                    width=width,
                    anchor="w",
                    cursor="hand2"
                )

                label.pack(
                    side="left",
                    padx=5,
                    pady=6
                )

                label.bind(
                    "<Button-1>",
                    lambda e,
                    sid=sale["id"],
                    r=row:
                    self.select_sale(sid, r)
                )

    def select_sale(self, sale_id, row):

        if self.selected_row is not None:

            try:
                self.selected_row.configure(
                    fg_color="#FFFFFF"
                )

            except Exception:
                pass

        row.configure(
            fg_color="#D9ECFF"
        )

        self.selected_row = row

        self.show_details(sale_id)

    # =========================
    # SHOW DETAILS
    # =========================
    def show_details(self, sale_id):

        try:

            data = self.sale_service.get_sale_details(sale_id)

            sale = data["sale"]
            items = data["items"]

            self.selected_sale_id = sale_id

            # =========================
            # Génère EXACTEMENT le même
            # ticket que l'impression
            # =========================

            ticket = self.sale_service.ticket_printer.generate(
                sale,
                items
            )

            self.details_text.configure(state="normal")
            self.details_text.delete("0.0", "end")
            self.details_text.insert("0.0", ticket)
            self.details_text.configure(state="disabled")

        except Exception as e:
            print("Details error:", e)

    # =========================
    # REPRINT
    # =========================
    def reprint_selected(self):

        if not self.selected_sale_id:
            print("No sale selected.")
            return

        try:
            data = self.sale_service.get_sale_details(self.selected_sale_id)

            ticket = self.sale_service.ticket_printer.generate(
                data["sale"],
                data["items"]
            )

            self.sale_service.last_ticket = ticket
            self.sale_service.thermal_printer.print_receipt(ticket)

            print("REPRINT DONE")

        except Exception as e:
            print("Reprint error:", e)
