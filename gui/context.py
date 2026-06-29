class UIContext:
    """
    Centralise services + controllers pour GUI POS.
    """

    def __init__(self, container):

        # =========================
        # DATABASE
        # =========================
        self.database = container.database


        # =========================
        # SERVICES
        # =========================
        self.sale_service = container.sale_service
        self.product_service = container.product_service
        self.export_service = container.export_service
        self.backup_service = container.backup_service

        # =========================
        # CONTROLLERS (GUI ENTRY POINT)
        # =========================
        self.product_controller = container.product_controller
        self.sale_controller = container.sale_controller
        self.event_bus = container.event_bus

        self.current_user = container.current_user
        self.current_role = container.current_role
        self.auth_service = container.auth_service
