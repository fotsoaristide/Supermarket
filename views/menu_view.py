from utils.formatter import Formatter


class MenuView:

    def display_menu(self):
        print("\n" + "=" * 50)
        print("       SUPERMARKET STOCK MANAGEMENT")
        print("=" * 50)
        print("1. Add Product")
        print("2. Display Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. New Sale")
        print("7. Sales History")
        print("8. Accounting")
        print("9. Quit")
        print("=" * 50)

    def get_choice(self):
        return input("\nYour choice : ")
    
    def show_error(self, message):
        print(f"\nError: {message}")

    def get_product_information(self):
        print("\n===== ADD  A PRODUCT =====")
        barcode = input("Barcode : ")
        name = input("Name : ")
        category = input("Category : ")

        purchase_price = float(
            input("Purchase Price : ")
        )
        selling_price = float(
            input("Selling Price : ")
        )
        quantity = int(
            input("Quantity : ")
        )
        minimum_stock = int(
            input("Minimum Stock(5 by default) : ") or 5
        )
        return (
            barcode,
            name,
            category,
            purchase_price,
            selling_price,
            quantity,
            minimum_stock
        )
     
    def success_message(self):
        print("\nProduct added successfully.")

    def error_message(self, message):
        print(f"\nErreur : {message}")

    def display_products(self, products):

        NAME_WIDTH = 35

        print("\n===== PRODUCTS LIST =====")
        print(f"{'ID':<4}{'BARCODE':<12}{'NAME':<35}{'PRICE':>10}   {'STOCK':>5}")
        print("-" * 75)

        for p in products:

            name_lines = Formatter.wrap_text(p.name, NAME_WIDTH)

            price = f"{p.selling_price:,.2f}".replace(",", " ")
            stock = str(p.quantity)

            # première ligne avec données
            print(
                f"{p.id:<4}"
                f"{p.barcode:<12}"
                f"{name_lines[0]:<35}"
                f"{price:>10}   "
                f"{stock:>5}"
            )

            # lignes suivantes = uniquement nom
            for line in name_lines[1:]:
                print(
                    f"{'':<4}"
                    f"{'':<12}"
                    f"{line:<35}"
                    f"{'':>10}   "
                    f"{'':>5}"
                )

        print("-" * 75)

    def invalid_choice(self):
        print("\nInvalid choice.")

    def get_delete_product_id(self):
        print("\n===== DELETE PRODUCT =====")
        return int(input("Enter Product ID to delete: "))

    def get_update_product_info(self):
        print("\n===== UPDATE PRODUCT =====")

        product_id = int(input("Product ID: "))
        barcode = input("Barcode: ")
        name = input("Name: ")
        category = input("Category: ")

        purchase_price = float(input("Purchase Price: "))
        selling_price = float(input("Selling Price: "))
        quantity = int(input("Quantity: "))
        minimum_stock = int(input("Minimum Stock: "))

        return (
            product_id,
            barcode,
            name,
            category,
            purchase_price,
            selling_price,
            quantity,
            minimum_stock
        )

    def goodbye(self):
        print("\nThank you for using the software.")
