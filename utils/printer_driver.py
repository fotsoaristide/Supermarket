from config.store_config import StoreConfig
from escpos.printer import Win32Raw


class PrinterDriver:
    """
    Windows thermal printer driver.
    """

    def __init__(self):
        try:
            self.printer = Win32Raw(
                StoreConfig.PRINTER_NAME
            )

        except Exception as e:
            print("[ERROR] Printer initialization:", e)
            self.printer = None

    def print_raw(self, text):
        """
        Print raw text to the thermal printer.
        """

        if self.printer is None:
            print("[ERROR] Printer unavailable")
            print(text)
            return

        self.printer.text(text)
        self.printer.cut()

        # Ferme correctement le job d'impression
        self.printer.close()
