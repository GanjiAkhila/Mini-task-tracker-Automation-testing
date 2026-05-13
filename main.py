import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from controllers.task_controller import TaskController
from repositories.task_repository import TaskRepository
from services.csv_export_service import CSVExportService
from services.validation_service import ValidationService
from styles.app_style import APP_STYLESHEET
from views.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLESHEET)

    base_dir = Path(__file__).resolve().parent
    database_path = base_dir / "tasks.db"

    repository = TaskRepository(database_path)
    validation_service = ValidationService()
    csv_export_service = CSVExportService()
    window = MainWindow()
    # Keep the controller alive for the full lifetime of the event loop.
    controller = TaskController(
        window, repository, validation_service, csv_export_service
    )

    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
