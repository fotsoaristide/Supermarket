import customtkinter as ctk
from gui.theme import Theme


class ProductCard(ctk.CTkFrame):
    """
    POS Modern Product Card (clean, Shopify/Square style)
    """

    def __init__(
        self,
        master,
        product,
        selected=False,
        on_select=None,
        on_delete=None,
        **kwargs
    ):
        super().__init__(
            master,
            corner_radius=12,
            border_width=1,
            border_color=Theme.BORDER,
            fg_color=Theme.SURFACE,
            **kwargs
        )

        self.product = product
        self.on_select = on_select
        self.on_delete = on_delete

        self.is_selected = selected

        self.configure_ui()
        self.build_ui()

    # =========================
    # STYLE UPDATE (SELECTION)
    # =========================
    def configure_ui(self):

        if self.is_selected:
            self.configure(
                border_color=Theme.PRIMARY,
                border_width=2
            )
        else:
            self.configure(
                border_color=Theme.BORDER,
                border_width=1
            )

    # =========================
    # UI BUILD
    # =========================
    def build_ui(self):

        # HEADER
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(10, 5))

        self.name_label = ctk.CTkLabel(
            header,
            text=self.product["name"],
            font=Theme.SUBTITLE,
            anchor="w",
            text_color=Theme.TEXT
        )
        self.name_label.pack(side="left", fill="x", expand=True)

        # OPTIONAL badge stock faible
        if self.product["stock"] <= 5:
            badge = ctk.CTkLabel(
                header,
                text="LOW",
                text_color="white",
                fg_color=Theme.WARNING,
                corner_radius=6,
                padx=6
            )
            badge.pack(side="right")

        # BARCODE
        barcode = self.product.get("barcode", "")

        self.barcode_label = ctk.CTkLabel(
            self,
            text=f"{barcode}",
            font=Theme.SMALL,
            text_color=Theme.TEXT_LIGHT,
            anchor="w"
        )
        self.barcode_label.pack(fill="x", padx=12)

        # FOOTER
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=12, pady=(8, 10))

        self.price_label = ctk.CTkLabel(
            footer,
            text=f"{self.product['price']} FCFA",
            font=Theme.BUTTON,
            text_color=Theme.PRIMARY
        )
        self.price_label.pack(side="left")

        stock_color = Theme.SUCCESS if self.product["stock"] > 5 else Theme.WARNING

        self.stock_label = ctk.CTkLabel(
            footer,
            text=f"Stock: {self.product['stock']}",
            text_color=stock_color
        )
        self.stock_label.pack(side="right")

        # DELETE BUTTON (DISCRET POS STYLE)
        self.delete_btn = ctk.CTkButton(
            self,
            text="Delete",
            width=30,
            height=28,
            fg_color="transparent",
            text_color=Theme.DANGER,
            hover_color=Theme.SURFACE,
            command=self._delete
        )
        self.delete_btn.place(relx=0.95, rely=0.1, anchor="ne")

        # =========================
        # CLICK EVENTS
        # =========================
        widgets = (
            self,
            header,
            self.name_label,
            self.barcode_label,
            footer,
            self.price_label,
            self.stock_label,
        )

        for w in widgets:
            w.bind("<Button-1>", self._select)

    # =========================
    # EVENTS
    # =========================
    def _select(self, event=None):

        if self.on_select:
            self.on_select(self.product)

    def _delete(self):

        if self.on_delete:
            self.on_delete(self.product)
