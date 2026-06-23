class MenuController:

    def __init__(self, container, menu_view, product_controller, sale_controller):
        self.container = container
        self.menu_view = menu_view
        self.product_controller = product_controller
        self.sale_controller = sale_controller

    def run(self):
        while True:

            self.menu_view.display_menu()

            choice = self.menu_view.get_choice()

            if choice == "1":
                self.product_controller.add_product()

            elif choice == "2":
                self.product_controller.display_products()

            elif choice == "3":
                self.product_controller.search_product()

            elif choice == "4":
                self.product_controller.update_product()

            elif choice == "5":
                self.product_controller.delete_product()

            elif choice == "6":
                self.handle_sale()

            elif choice == "7":
                self.sale_controller.show_sales_history()

            elif choice == "8":
                self.sale_controller.accounting_menu()

            elif choice == "9":
                self.export_data_menu()

            elif choice == "10":
                self.backup_menu()

            elif choice == "11":
                break

            else:
                self.menu_view.show_error("Invalid choice")

    # =========================
    # SALES FLOW
    # =========================
    def handle_sale(self):
        self.sale_controller.start_sale()

        while True:
            self.sale_controller.sale_view.show_sale_menu()

            choice = input("Choice: ")

            if choice == "1":
                self.sale_controller.add_product()

            elif choice == "2":
                self.sale_controller.show_current_sale()

            elif choice == "3":
                self.sale_controller.update_item_quantity()

            elif choice == "4":
                self.sale_controller.remove_product()

            elif choice == "5":
                self.sale_controller.cancel_sale()
                break

            elif choice == "6":
                self.sale_controller.end_sale()
                break

            else:
                print("Invalid choice")

    def export_data_menu(self):
        """
        Handle all export operations (CSV).
        """

        while True:
            print("\n===== EXPORT DATA =====")
            print("1. Export Products")
            print("2. Export Sales")
            print("3. Back")

            choice = input("Choice: ")

            try:
                if choice == "1":
                    path = self.container.export_service.export_products()
                    print(f"✅ Products exported: {path}")

                elif choice == "2":
                    path = self.container.export_service.export_sales()
                    print(f"✅ Sales exported: {path}")

                elif choice == "3":
                    break

                else:
                    print("Invalid choice")

            except Exception as e:
                print(f"❌ Export error: {e}")

    def backup_menu(self):
        """
        Handle database backup and restore.
        """

        while True:
            print("\n===== BACKUP SYSTEM =====")
            print("1. Create backup")
            print("2. Restore backup")
            print("3. Back")

            choice = input("Choice: ")

            try:
                if choice == "1":
                    path = self.container.backup_service.create_backup()
                    print(f"✅ Backup created: {path}")

                elif choice == "2":
                    backups = self.container.backup_service.list_backups()

                    if not backups:
                        print("No backup available.")
                        return

                    print("\n===== AVAILABLE BACKUPS =====")

                    for i, b in enumerate(backups):
                        print(f"{i + 1}. {b}")

                    try:
                        index = int(input("Select backup number: ")) - 1
                        selected_backup = backups[index]

                        self.container.backup_service.restore_backup(selected_backup)

                        print("✅ Database restored successfully")

                    except (IndexError, ValueError):
                        print("❌ Invalid selection")

                elif choice == "3":
                    break

                else:
                    print("Invalid choice")

            except Exception as e:
                print(f"❌ Backup error: {e}")
