from services.validation_service import ValidationService


def test_empty_title_is_invalid() -> None:
    service = ValidationService()

    errors = service.validate_task(title="", priority="High", status="Todo")

    assert "Title cannot be empty." in errors


def test_title_with_only_spaces_is_invalid() -> None:
    service = ValidationService()

    errors = service.validate_task(title="   ", priority="High", status="Todo")

    assert "Title cannot be empty." in errors


def test_missing_priority_is_invalid() -> None:
    service = ValidationService()

    errors = service.validate_task(title="Build UI", priority="", status="Todo")

    assert "Priority must be selected." in errors


def test_placeholder_priority_is_invalid() -> None:
    service = ValidationService()

    errors = service.validate_task(
        title="Build UI", priority="Select priority", status="Todo"
    )

    assert "Priority must be selected." in errors


def test_missing_status_is_invalid() -> None:
    service = ValidationService()

    errors = service.validate_task(title="Build UI", priority="Medium", status="")

    assert "Status must be selected." in errors


def test_placeholder_status_is_invalid() -> None:
    service = ValidationService()

    errors = service.validate_task(
        title="Build UI", priority="Medium", status="Select status"
    )

    assert "Status must be selected." in errors


def test_valid_task_input_passes_validation() -> None:
    service = ValidationService()

    errors = service.validate_task(
        title="Build UI",
        priority="Low",
        status="In Progress",
    )

    assert errors == []
