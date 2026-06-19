"""Database module."""

from pathlib import Path
import sqlite3


class Database:
    """Database class for managing SQLite connections."""

    def __init__(self, db_name="stock.db"):

        database_path = (
            Path(__file__).parent / "stock.db"
        )
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
