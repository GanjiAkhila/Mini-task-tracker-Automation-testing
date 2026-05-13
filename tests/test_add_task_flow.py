from pathlib import Path

from PySide6.QtWidgets import QApplication

from controllers.task_controller import TaskController
from repositories.task_repository import TaskRepository
from services.validation_service import ValidationService
from views.main_window import MainWindow


def _get_app() -> QApplication:
    app = QApplication.instance()
    return app if app is not None else QApplication([])


def test_add_task_updates_table_and_database(tmp_path: Path) -> None:
    _get_app()
    database_path = tmp_path / "tasks.db"

    repository = TaskRepository(database_path)
    window = MainWindow()
    controller = TaskController(window, repository, ValidationService())

    window.task_form.title_input.setText("Implement add task flow")
    window.task_form.description_input.setPlainText("Verify controller and repository")
    window.task_form.priority_input.setCurrentText("High")
    window.task_form.status_input.setCurrentText("Todo")

    window.task_form.submit_button.click()

    assert window.task_table.rowCount() == 1
    assert repository.get_all_tasks()[0].title == "Implement add task flow"

    window.close()
    del controller


def test_existing_tasks_load_when_app_starts(tmp_path: Path) -> None:
    _get_app()
    database_path = tmp_path / "tasks.db"

    first_repository = TaskRepository(database_path)
    window_one = MainWindow()
    controller_one = TaskController(window_one, first_repository, ValidationService())

    window_one.task_form.title_input.setText("Persisted task")
    window_one.task_form.priority_input.setCurrentText("Medium")
    window_one.task_form.status_input.setCurrentText("In Progress")
    window_one.task_form.submit_button.click()

    second_repository = TaskRepository(database_path)
    window_two = MainWindow()
    controller_two = TaskController(window_two, second_repository, ValidationService())

    assert window_two.task_table.rowCount() == 1
    assert window_two.task_table.item(0, 1).text() == "Persisted task"

    window_one.close()
    window_two.close()
    del controller_one
    del controller_two


def test_edit_keeps_description_and_updates_values(tmp_path: Path) -> None:
    _get_app()
    database_path = tmp_path / "tasks.db"

    repository = TaskRepository(database_path)
    window = MainWindow()
    controller = TaskController(window, repository, ValidationService())

    window.task_form.title_input.setText("Editable task")
    window.task_form.description_input.setPlainText("Initial description")
    window.task_form.priority_input.setCurrentText("Low")
    window.task_form.status_input.setCurrentText("Todo")
    window.task_form.submit_button.click()

    window.task_table.selectRow(0)
    controller.edit_selected_task()
    assert window.task_form.description_input.toPlainText() == "Initial description"

    window.task_form.description_input.setPlainText("Updated description")
    window.task_form.status_input.setCurrentText("Done")
    window.task_form.submit_button.click()

    saved_task = repository.get_all_tasks()[0]
    assert saved_task.description == "Updated description"
    assert saved_task.status == "Done"

    window.close()
    del controller
