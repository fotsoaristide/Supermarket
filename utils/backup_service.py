import os
import shutil
from datetime import datetime


class BackupService:
    """
    Handles SQLite database backup and restore.
    """

    def __init__(self, db_path):
        self.db_path = db_path

    def create_backup(self):
        """
        Create a timestamped backup of SQLite database.
        """

        if not os.path.exists(self.db_path):
            raise Exception(f"Database not found: {self.db_path}")

        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        backup_path = os.path.join(
            backup_dir,
            f"backup_{timestamp}.db"
        )

        shutil.copy2(self.db_path, backup_path)

        return backup_path

    def restore_backup(self, backup_file):
        """
        Restore database from backup file.
        """

        if not os.path.exists(backup_file):
            raise Exception("Backup file not found")

        shutil.copy2(backup_file, self.db_path)

        return True

    def list_backups(self):
        """
        Return all available backup files.
        """

        backup_dir = "backups"

        if not os.path.exists(backup_dir):
            return []

        files = [
            os.path.join(backup_dir, f)
            for f in os.listdir(backup_dir)
            if f.endswith(".db")
        ]

        # tri du plus récent au plus ancien
        files.sort(reverse=True)

        return files
