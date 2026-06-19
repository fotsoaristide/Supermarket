from database.database import Database
from repositories.product_repository import ProductRepository
from services.product_service import ProductService
from views.menu_view import MenuView
from controllers.product_controller import ProductController
from controllers.menu_controller import MenuController


class Container:

    def __init__(self):

        # Infrastructure
        self.database = Database()

        # Repositories
        self.product_repository = ProductRepository(
            self.database
        )

        # Services
        self.product_service = ProductService(
            self.product_repository
        )

        # Views
        self.menu_view = MenuView()

        # Controllers
        self.product_controller = ProductController(
            self.product_service,
            self.menu_view
        )

        self.menu_controller = MenuController(
            self.menu_view,
            self.product_controller
        )

    @property
    def app(self):
        return self.menu_controller