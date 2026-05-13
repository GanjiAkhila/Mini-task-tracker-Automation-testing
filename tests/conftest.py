import pytest
from pathlib import Path
from PySide6.QtWidgets import QApplication
from unittest.mock import MagicMock

from repositories.task_repository import TaskRepository
from services.validation_service import ValidationService
from services.csv_export_service import CSVExportService
from controllers.task_controller import TaskController
from views.main_window import MainWindow

@pytest.fixture(scope="session")
def app():
    """Provides a single QApplication instance for the entire test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # No explicit quit to avoid crashing session, PySide6 handles cleanup

@pytest.fixture
def db_path(tmp_path):
    """Provides a temporary path for the SQLite database."""
    return tmp_path / "test_tasks.db"

@pytest.fixture
def repository(db_path):
    """Provides a TaskRepository instance using a temporary database."""
    return TaskRepository(db_path)

@pytest.fixture
def validation_service():
    """Provides a fresh ValidationService instance."""
    return ValidationService()

@pytest.fixture
def csv_export_service():
    """Provides a fresh CSVExportService instance."""
    return CSVExportService()

@pytest.fixture
def main_window(app):
    """Provides a MainWindow instance."""
    window = MainWindow()
    yield window
    window.close()

@pytest.fixture
def controller(main_window, repository, validation_service, csv_export_service):
    """Provides a TaskController wired with test components."""
    return TaskController(
        main_window, 
        repository, 
        validation_service, 
        csv_export_service
    )

@pytest.fixture
def mock_view():
    """Provides a mocked MainWindow for controller unit testing."""
    view = MagicMock(spec=MainWindow)
    # Mock signals/widgets that the controller connects to
    view.task_form = MagicMock()
    view.task_form.submit_button = MagicMock()
    view.task_form.clear_button = MagicMock()
    view.edit_button = MagicMock()
    view.delete_button = MagicMock()
    view.refresh_button = MagicMock()
    view.export_button = MagicMock()
    view.apply_filter_button = MagicMock()
    view.clear_filter_button = MagicMock()
    view.sort_order_combo = MagicMock()
    view.search_input = MagicMock()
    
    # Default return values for common methods
    view.get_filter_values.return_value = {
        "status": "",
        "priority": "",
        "title_query": "",
        "sort_order": "desc"
    }
    return view
