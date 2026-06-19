"""Database module."""

from pathlib import Path
import sqlite3
from database.schema import SALES_TABLE, SALE_ITEMS_TABLE


class Database:
    """Database class for managing SQLite connections."""

    def __init__(self, db_name="stock.db"):

        database_path = Path(__file__).parent / db_name

        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def init_db(self):
        self.cursor.execute(SALES_TABLE)
        self.cursor.execute(SALE_ITEMS_TABLE)
        self.connection.commit()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
