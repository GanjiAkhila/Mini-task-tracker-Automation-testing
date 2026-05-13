import pytest
from unittest.mock import MagicMock
from models.task import Task
from controllers.task_controller import TaskController

def test_controller_add_task_calls_repository(mock_view, repository, validation_service):
    # Setup mock view data
    mock_view.task_form.get_form_data.return_value = {
        "title": "Test Task",
        "description": "Test Desc",
        "priority": "High",
        "status": "Todo"
    }
    
    # Initialize controller with mock view
    controller = TaskController(mock_view, repository, validation_service)
    
    # Trigger add_task
    controller.add_task()
    
    # Verify repository call
    tasks = repository.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    
    # Verify view update call
    mock_view.populate_tasks.assert_called()

def test_controller_shows_error_on_invalid_data(mock_view, repository, validation_service):
    # Setup invalid data
    mock_view.task_form.get_form_data.return_value = {
        "title": "",
        "description": "",
        "priority": "High",
        "status": "Todo"
    }
    
    controller = TaskController(mock_view, repository, validation_service)
    controller.add_task()
    
    # Verify repository was NOT called for insert
    assert len(repository.get_all_tasks()) == 0
    
    # Verify error was shown
    mock_view.show_error.assert_called_with("Title cannot be empty.")

def test_controller_delete_task_with_confirmation(mock_view, repository, validation_service):
    # Add a task to delete
    task_id = repository.add_task(Task(title="Delete Me", priority="Low", status="Todo"))
    
    mock_view.get_selected_task_id.return_value = task_id
    mock_view.ask_delete_confirmation.return_value = True
    
    controller = TaskController(mock_view, repository, validation_service)
    controller.delete_selected_task()
    
    # Verify deletion
    assert repository.get_task_by_id(task_id) is None
    mock_view.ask_delete_confirmation.assert_called_once_with("Delete Me")

def test_controller_delete_task_cancelled(mock_view, repository, validation_service):
    task_id = repository.add_task(Task(title="Keep Me", priority="Low", status="Todo"))
    
    mock_view.get_selected_task_id.return_value = task_id
    mock_view.ask_delete_confirmation.return_value = False
    
    controller = TaskController(mock_view, repository, validation_service)
    controller.delete_selected_task()
    
    # Verify task still exists
    assert repository.get_task_by_id(task_id) is not None
