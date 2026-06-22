"""
Common formatting utilities.

This module centralizes every formatting function
used across the application.
"""

from datetime import datetime
import textwrap

from config.store_config import StoreConfig


class Formatter:
    """
    Shared formatting utilities.
    """

    @staticmethod
    def format_money(amount):
        """
        Format monetary value.

        Example:
            3250 -> 3 250 FCFA
        """
        value = f"{amount:,.0f}".replace(",", " ")
        return f"{value} {StoreConfig.STORE_CURRENCY}"

    @staticmethod
    def format_date(iso_date):
        """
        Convert ISO date into human readable format.
        """

        dt = datetime.fromisoformat(iso_date)

        return dt.strftime("%d/%m/%Y %H:%M")

    @staticmethod
    def wrap_text(text, width):
        """
        Wrap text according to receipt width.
        """

        return textwrap.wrap(
            text.upper(),
            width=width
        )
