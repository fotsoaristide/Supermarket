"""
Store configuration.

Contains all information related to the business.
"""


class StoreConfig:
    """
    Centralized store configuration.
    """

    # ==========================================
    # BUSINESS IDENTITY
    # ==========================================

    STORE_NAME = "NB MINI-MARKET"

    STORE_SLOGAN = (
        "Votre mini-marche de confiance !"
    )

    STORE_ADDRESS = (
        "Souza - Cameroun"
    )

    STORE_PHONE = "+237 682 454 030"

    STORE_EMAIL = ""

    STORE_CITY = "Souza"

    STORE_COUNTRY = "Cameroon"

    BUSINESS_REGISTRATION = ""

    TAX_NUMBER = ""

    # ==========================================
    # RECEIPT SETTINGS
    # ==========================================

    STORE_CURRENCY = "FCFA"

    RECEIPT_WIDTH = 32

    FOOTER_MESSAGE = (
        "Merci pour votre confiance !"
    )

    SHOW_EMAIL = False

    SHOW_PHONE = True

    SHOW_ADDRESS = True

    # =========================
    # PRINTER
    # =========================

    PRINTER_NAME = "XP-58 (copy 1)"
