import pytest
from services.validation_service import ValidationService

@pytest.fixture
def service():
    return ValidationService()

def test_validate_task_all_fields_valid(service):
    errors = service.validate_task(title="Fix Bug", priority="High", status="Todo")
    assert not errors

def test_validate_task_empty_title(service):
    errors = service.validate_task(title="", priority="High", status="Todo")
    assert "Title cannot be empty." in errors

def test_validate_task_whitespace_title(service):
    errors = service.validate_task(title="   ", priority="High", status="Todo")
    assert "Title cannot be empty." in errors

def test_validate_task_invalid_priority_empty(service):
    errors = service.validate_task(title="Fix Bug", priority="", status="Todo")
    assert "Priority must be selected." in errors

def test_validate_task_invalid_priority_placeholder(service):
    errors = service.validate_task(title="Fix Bug", priority="Select priority", status="Todo")
    assert "Priority must be selected." in errors

def test_validate_task_invalid_priority_whitespace(service):
    # Testing strip() logic for priority
    errors = service.validate_task(title="Fix Bug", priority=" Select priority ", status="Todo")
    assert "Priority must be selected." in errors

def test_validate_task_invalid_status_empty(service):
    errors = service.validate_task(title="Fix Bug", priority="High", status="")
    assert "Status must be selected." in errors

def test_validate_task_invalid_status_placeholder(service):
    errors = service.validate_task(title="Fix Bug", priority="High", status="Select status")
    assert "Status must be selected." in errors

def test_validate_task_invalid_status_whitespace(service):
    # Testing strip() logic for status
    errors = service.validate_task(title="Fix Bug", priority="High", status="  Select status  ")
    assert "Status must be selected." in errors

def test_validate_task_multiple_errors(service):
    errors = service.validate_task(title="", priority="", status="")
    assert len(errors) == 3
    assert "Title cannot be empty." in errors
    assert "Priority must be selected." in errors
    assert "Status must be selected." in errors
