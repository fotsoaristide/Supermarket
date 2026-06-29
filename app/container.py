from database.database import Database
from repositories.product_repository import ProductRepository
from services.product_service import ProductService
from views.menu_view import MenuView
from controllers.product_controller import ProductController
from controllers.menu_controller import MenuController
from repositories.sale_repository import SaleRepository
from services.sale_service import SaleService
from controllers.sale_controller import SaleController
from views.sale_view import SaleView
from utils.export_service import ExportService
from utils.backup_service import BackupService
from utils.event_bus import EventBus
from services.auth_service import AuthService


class Container:

    def __init__(self):

        self.database = Database()
        self.database.init_db()

        self.event_bus = EventBus()

        self.export_service = ExportService(self.database)

        self.backup_service = BackupService(
            self.database.db_path
        )

        self.product_repository = ProductRepository(self.database)

        self.product_service = ProductService(
            self.product_repository
        )

        self.menu_view = MenuView()

        self.product_controller = ProductController(
            self.product_service,
            self.menu_view,
            self.event_bus
        )

        self.sale_repository = SaleRepository(self.database)

        self.sale_service = SaleService(
            self.sale_repository,
            self.product_repository
        )

        self.sale_service.event_bus = self.event_bus

        self.sale_view = SaleView()

        self.sale_controller = SaleController(
            self.sale_service,
            self.product_service,
            self.sale_view
        )

        self.menu_controller = MenuController(
            self,
            self.menu_view,
            self.product_controller,
            self.sale_controller
        )

        self.current_user = None
        self.current_role = None
        self.auth_service = AuthService()

    @property
    def app(self):
        return self.menu_controller
