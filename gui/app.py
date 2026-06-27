import customtkinter as ctk

from gui.context import UIContext
from gui.widgets.sidebar import Sidebar
from gui.widgets.topbar import TopBar

from gui.views.dashboard_view import DashboardView
from gui.views.products_view import ProductsView
from gui.views.sales_view import SalesView
from gui.views.history_view import HistoryView
from gui.views.accounting_view import AccountingView
from gui.views.export_view import ExportView
from gui.views.backup_view import BackupView
from gui.views.settings_view import SettingsView

from gui.theme import Theme


class App(ctk.CTk):

    def __init__(self, container):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Supermarket POS")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        self.configure(fg_color=Theme.BACKGROUND)

        # BACKEND
        self.container = container
        self.ui = UIContext(container)

        # =========================
        # GLOBAL GRID LAYOUT FIX
        # =========================
        self.grid_columnconfigure(0, weight=0)  # sidebar fixed
        self.grid_columnconfigure(1, weight=1)  # content FULL WIDTH
        self.grid_rowconfigure(1, weight=1)     # content row expand

        # SIDEBAR
        self.sidebar = Sidebar(self, self.show_page)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        # TOPBAR
        self.topbar = TopBar(self)
        self.topbar.grid(row=0, column=1, sticky="ew")

        # CONTENT AREA (IMPORTANT FIX)
        self.content = ctk.CTkFrame(self, fg_color=Theme.BACKGROUND)
        self.content.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)

        # IMPORTANT: allow pages to stretch inside content
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # PAGES
        self.pages = {}
        self.register_pages()

        self.show_page("Dashboard")

    def register_pages(self):

        self.pages = {
            "Dashboard": DashboardView(self.content, self.ui),
            "Products": ProductsView(self.content, self.ui),
            "Sales": SalesView(self.content, self.ui),
            "History": HistoryView(self.content, self.ui),
            "Accounting": AccountingView(self.content, self.ui),
            "Export": ExportView(self.content, self.ui),
            "Backup": BackupView(self.content, self.ui),
            "Settings": SettingsView(self.content, self.ui),
        }

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name):
        self.pages[page_name].tkraise()
