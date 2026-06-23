from utils.printer_driver import PrinterDriver


class ThermalPrinter:
    """
    Handles receipt output to physical printer.
    """

    def __init__(self, mode="console"):
        self.mode = mode
        self.driver = PrinterDriver()

    def print_receipt(self, receipt):

        if self.mode == "console":
            self._print_console(receipt)

        elif self.mode == "usb":
            self._print_usb(receipt)

        else:
            raise ValueError("Unknown printer mode")

    def _print_console(self, receipt):
        print("\n" + "=" * 40)
        print("THERMAL PRINTER (SIMULATION)")
        print("=" * 40)
        print(receipt)
        print("=" * 40)

    def _print_usb(self, receipt):
        self.driver.print_raw(receipt)
