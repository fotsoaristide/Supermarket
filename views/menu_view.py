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
        print("7. Quit")
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

        print("\n===== PRODUCTS LIST =====")

        if not products:
            print("No products registered.")
            return

        print(f"{'ID':<5}{'CODE':<15}{'NOM':<25}{'PRIX':<12}{'STOCK'}")
        print("-" * 70)

        for product in products:

            print(
                f"{product.id:<5}"
                f"{product.barcode:<15}"
                f"{product.name:<25}"
                f"{product.selling_price:<12.2f}"
                f"{product.quantity:<10}"
            )

    def invalid_choice(self):
        print("\nInvalid choice.")

    def goodbye(self):
        print("\nThank you for using the software.")
