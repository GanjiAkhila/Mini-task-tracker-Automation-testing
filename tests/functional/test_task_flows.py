from repositories.task_repository import TaskRepository
from controllers.task_controller import TaskController

def test_add_task_updates_table_and_database(main_window, repository, controller) -> None:
    main_window.task_form.title_input.setText("Implement add task flow")
    main_window.task_form.description_input.setPlainText("Verify controller and repository")
    main_window.task_form.priority_input.setCurrentText("High")
    main_window.task_form.status_input.setCurrentText("Todo")

    main_window.task_form.submit_button.click()

    assert main_window.task_table.rowCount() == 1
    assert repository.get_all_tasks()[0].title == "Implement add task flow"


def test_existing_tasks_load_when_app_starts(db_path, validation_service) -> None:
    # First app session
    first_repository = TaskRepository(db_path)
    # Use direct creation for session-specific tests if needed, or stick to logic
    # But for a "flow" test of persistence, we can simulate two sessions
    
    task_data = {
        "title": "Persisted task",
        "priority": "Medium",
        "status": "In Progress"
    }
    
    from models.task import Task
    first_repository.add_task(Task(**task_data))

    # Second app session
    from views.main_window import MainWindow
    second_window = MainWindow()
    second_repository = TaskRepository(db_path)
    _controller = TaskController(second_window, second_repository, validation_service)

    assert second_window.task_table.rowCount() == 1
    assert second_window.task_table.item(0, 1).text() == "Persisted task"
    second_window.close()


def test_edit_keeps_description_and_updates_values(main_window, repository, controller) -> None:
    main_window.task_form.title_input.setText("Editable task")
    main_window.task_form.description_input.setPlainText("Initial description")
    main_window.task_form.priority_input.setCurrentText("Low")
    main_window.task_form.status_input.setCurrentText("Todo")
    main_window.task_form.submit_button.click()

    main_window.task_table.selectRow(0)
    controller.edit_selected_task()
    assert main_window.task_form.description_input.toPlainText() == "Initial description"

    main_window.task_form.description_input.setPlainText("Updated description")
    main_window.task_form.status_input.setCurrentText("Done")
    main_window.task_form.submit_button.click()

    saved_task = repository.get_all_tasks()[0]
    assert saved_task.description == "Updated description"
    assert saved_task.status == "Done"
