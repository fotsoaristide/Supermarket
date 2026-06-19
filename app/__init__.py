from database.database import Database
from repositories.product_repository import ProductRepository
from services.product_service import ProductService
from controllers.product_controller import ProductController
from controllers.menu_controller import MenuController
from views.menu_view import MenuView


def main():

    database = Database()

    repository = ProductRepository(database)

    service = ProductService(repository)

    view = MenuView()

    product_controller = ProductController(
        service,
        view
    )

    menu_controller = MenuController(
        view,
        product_controller
    )

    menu_controller.run()


if __name__ == "__main__":
    main()