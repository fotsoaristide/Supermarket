import customtkinter as ctk
from gui.views.base_view import BaseView
from gui.theme import Theme


class ExportView(BaseView):

    def __init__(self, master, ui):
        super().__init__(master, "Export")

        self.ui = ui

        self.build_ui()

    def build_ui(self):

        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_rowconfigure(1, weight=1)

        # =========================
        # EXPORT SETTINGS
        # =========================

        self.settings_frame = ctk.CTkFrame(
            self.body,
            corner_radius=12
        )
        self.settings_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            self.settings_frame,
            text="EXPORT CENTER",
            font=("Arial", 20, "bold"),
            text_color=Theme.PRIMARY
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

        self.export_category = ctk.CTkOptionMenu(
            self.settings_frame,
            values=[
                "Sales",
                "Inventory",
                "Accounting"
            ]
        )
        self.export_category.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.export_report = ctk.CTkOptionMenu(
            self.settings_frame,
            values=[
                "Daily Report",
                "Weekly Report",
                "Monthly Report",
                "Profit Report",
                "Top Selling Products",
                "Unsold Products",
                "Stock Valuation",
                "Sales History"
            ]
        )
        self.export_report.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.export_format = ctk.CTkOptionMenu(
            self.settings_frame,
            values=[
                "CSV",
                "JSON",
                "TXT"
            ]
        )
        self.export_format.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.start_date = ctk.CTkEntry(
            self.settings_frame,
            placeholder_text="Start date DD/MM/YYYY"
        )
        self.start_date.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.end_date = ctk.CTkEntry(
            self.settings_frame,
            placeholder_text="End date DD/MM/YYYY"
        )
        self.end_date.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # =========================
        # AVAILABLE EXPORTS
        # =========================

        self.preview_frame = ctk.CTkFrame(
            self.body,
            corner_radius=12
        )
        self.preview_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            self.preview_frame,
            text="AVAILABLE DATA",
            font=("Arial",18,"bold"),
            text_color=Theme.PRIMARY
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

        exports = [
            "Sales",
            "Profit",
            "Inventory",
            "Top Products",
            "Unsold Products"
        ]

        for item in exports:

            ctk.CTkCheckBox(
                self.preview_frame,
                text=item
            ).pack(
                anchor="w",
                padx=25,
                pady=5
            )

        # =========================
        # ACTIONS
        # =========================

        self.action_frame = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )
        self.action_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        self.export_btn = ctk.CTkButton(
            self.action_frame,
            text="EXPORT",
            height=45,
            fg_color=Theme.PRIMARY,
            command=self.confirm_export
        )
        self.export_btn.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        self.folder_btn = ctk.CTkButton(
            self.action_frame,
            text="OPEN EXPORT FOLDER",
            height=45,
            command=self.open_exports
        )
        self.folder_btn.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        self.status_label = ctk.CTkLabel(
            self.body,
            text="Ready to export",
            font=("Arial",14)
        )
        self.status_label.grid(
            row=3,
            column=0,
            pady=10
        )

    def open_exports(self):

        if not self.confirm_action(
            "Open Folder",
            "Open exports folder ?"
        ):
            return

        import os

        path = "exports"

        os.makedirs(
            path,
            exist_ok=True
        )

        os.startfile(path)

    def confirm_action(
        self,
        title,
        message
    ):

        dialog = ctk.CTkToplevel(self)

        dialog.title(title)
        dialog.geometry("340x180")
        dialog.grab_set()

        dialog.update_idletasks()

        x = (
            dialog.winfo_screenwidth() // 2
            - 340 // 2
        )

        y = (
            dialog.winfo_screenheight() // 2
            - 180 // 2
        )

        dialog.geometry(
            f"340x180+{x}+{y}"
        )

        result = {"ok": False}

        ctk.CTkLabel(
            dialog,
            text=message,
            font=("Arial", 15)
        ).pack(
            pady=30
        )

        buttons = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=20,
            pady=10
        )

        def yes():
            result["ok"] = True
            dialog.destroy()

        def no():
            dialog.destroy()

        ctk.CTkButton(
            buttons,
            text="YES",
            command=yes
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="NO",
            command=no
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        dialog.wait_window()

        return result["ok"]

    def export_data(self):

        try:

            service = self.ui.export_service

            category = self.export_category.get()
            report = self.export_report.get()

            # =========================
            # INVENTORY EXPORTS
            # =========================

            if category == "Inventory":

                path = service.export_products()

            # =========================
            # SALES EXPORTS
            # =========================

            elif category == "Sales":

                path = service.export_sales()

            # =========================
            # ACCOUNTING EXPORTS
            # =========================

            else:

                if report == "Daily Report":

                    data = self.ui.sale_service.get_daily_report()

                elif report == "Weekly Report":

                    data = self.ui.sale_service.get_weekly_report()

                elif report == "Monthly Report":

                    data = self.ui.sale_service.get_monthly_report()

                elif report == "Profit Report":

                    data = self.ui.sale_service.get_profit_report()

                elif report == "Top Selling Products":

                    data = self.ui.sale_service.get_top_selling_report()

                elif report == "Unsold Products":

                    data = self.ui.sale_service.get_unsold_report()

                else:

                    raise Exception(
                        "Unknown accounting report."
                    )

                import os
                import csv
                import json
                from datetime import datetime

                os.makedirs(
                    "exports",
                    exist_ok=True
                )

                fmt = self.export_format.get()

                filename = (
                    report.lower()
                    .replace(" ", "_")
                )

                filename += "_"

                filename += datetime.now().strftime(
                    "%Y-%m-%d_%H-%M-%S"
                )

                # =========================
                # CSV
                # =========================

                if fmt == "CSV":

                    path = f"exports/{filename}.csv"

                    with open(
                        path,
                        "w",
                        newline="",
                        encoding="utf-8-sig"
                    ) as f:

                        writer = csv.writer(
                            f,
                            delimiter=';'
                        )

                        if "items" in data:

                            if data["items"]:

                                first = data["items"][0]

                                if isinstance(first, dict):

                                    writer.writerow(
                                        first.keys()
                                    )

                                    for item in data["items"]:
                                        writer.writerow(
                                            item.values()
                                        )

                                else:

                                    writer.writerow(
                                        ["Product"]
                                    )

                                    for item in data["items"]:
                                        writer.writerow(
                                            [item.name]
                                        )

                        else:

                            for k, v in data.items():

                                writer.writerow(
                                    [k, v]
                                )

                # =========================
                # JSON
                # =========================

                elif fmt == "JSON":

                    path = f"exports/{filename}.json"

                    with open(
                        path,
                        "w",
                        encoding="utf-8"
                    ) as f:

                        json.dump(
                            data,
                            f,
                            indent=4,
                            default=str
                        )

                # =========================
                # TXT
                # =========================

                else:

                    path = f"exports/{filename}.txt"

                    with open(
                        path,
                        "w",
                        encoding="utf-8"
                    ) as f:

                        for k, v in data.items():

                            f.write(
                                f"{k}: {v}\n"
                            )

            self.status_label.configure(
                text=f"Export successful: {path}"
            )

        except Exception as e:

            print(
                "Export error:",
                e
            )

            self.status_label.configure(
                text="Export failed"
            )
    
    def confirm_export(self):

        if hasattr(self, "confirm_window"):

            if self.confirm_window.winfo_exists():
                self.confirm_window.focus()
                return

        self.confirm_window = ctk.CTkToplevel(self)

        self.confirm_window.title("Confirm Export")
        self.confirm_window.geometry("350x160")
        self.confirm_window.grab_set()

        ctk.CTkLabel(
            self.confirm_window,
            text="Export selected report ?",
            font=("Arial",16,"bold")
        ).pack(pady=20)

        buttons = ctk.CTkFrame(
            self.confirm_window,
            fg_color="transparent"
        )
        buttons.pack(pady=10)

        ctk.CTkButton(
            buttons,
            text="YES",
            width=100,
            command=lambda: [
                self.confirm_window.destroy(),
                self.export_data()
            ]
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons,
            text="NO",
            width=100,
            command=self.confirm_window.destroy
        ).pack(side="left", padx=10)
    
    def confirm_open_folder(self):

        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm")
        dialog.geometry("300x150")
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Open export folder ?",
            font=("Arial",15,"bold")
        ).pack(pady=25)

        buttons = ctk.CTkFrame(dialog)
        buttons.pack(fill="x", padx=15, pady=10)

        ctk.CTkButton(
            buttons,
            text="YES",
            command=lambda: (
                dialog.destroy(),
                self.open_exports()
            )
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="NO",
            command=dialog.destroy
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )
