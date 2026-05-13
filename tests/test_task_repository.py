import sqlite3
from pathlib import Path

from models.task import Task
from repositories.task_repository import TaskRepository


def _create_repository(tmp_path: Path) -> tuple[Path, TaskRepository]:
    database_path = tmp_path / "tasks.db"
    return database_path, TaskRepository(database_path)


def test_create_table_works(tmp_path: Path) -> None:
    database_path, _repository = _create_repository(tmp_path)

    with sqlite3.connect(database_path) as connection:
        table = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'tasks'"
        ).fetchone()

    assert table is not None


def test_insert_and_fetch_tasks_work(tmp_path: Path) -> None:
    _database_path, repository = _create_repository(tmp_path)
    repository.add_task(
        Task(
            title="Build repository tests",
            description="Insert and fetch",
            priority="High",
            status="Todo",
        )
    )

    tasks = repository.get_all_tasks()

    assert len(tasks) == 1
    assert tasks[0].title == "Build repository tests"
    assert tasks[0].description == "Insert and fetch"


def test_update_task_works(tmp_path: Path) -> None:
    _database_path, repository = _create_repository(tmp_path)
    task_id = repository.add_task(
        Task(
            title="Initial task",
            description="Original description",
            priority="Low",
            status="Todo",
        )
    )

    repository.update_task(
        Task(
            id=task_id,
            title="Updated task",
            description="Updated description",
            priority="Medium",
            status="Done",
            created_at=repository.get_task_by_id(task_id).created_at,  # type: ignore[union-attr]
        )
    )

    task = repository.get_task_by_id(task_id)

    assert task is not None
    assert task.title == "Updated task"
    assert task.description == "Updated description"
    assert task.priority == "Medium"
    assert task.status == "Done"


def test_delete_task_works(tmp_path: Path) -> None:
    _database_path, repository = _create_repository(tmp_path)
    task_id = repository.add_task(
        Task(
            title="Delete me",
            description="Delete test",
            priority="Low",
            status="Todo",
        )
    )

    repository.delete_task(task_id)

    assert repository.get_task_by_id(task_id) is None


def test_filter_by_status_works(tmp_path: Path) -> None:
    _database_path, repository = _create_repository(tmp_path)
    repository.add_task(
        Task(title="Todo task", description="", priority="High", status="Todo")
    )
    repository.add_task(
        Task(title="Done task", description="", priority="Low", status="Done")
    )

    tasks = repository.filter_tasks(status="Done")

    assert len(tasks) == 1
    assert tasks[0].title == "Done task"


def test_filter_by_priority_works(tmp_path: Path) -> None:
    _database_path, repository = _create_repository(tmp_path)
    repository.add_task(
        Task(title="High priority", description="", priority="High", status="Todo")
    )
    repository.add_task(
        Task(title="Medium priority", description="", priority="Medium", status="Todo")
    )

    tasks = repository.filter_tasks(priority="High")

    assert len(tasks) == 1
    assert tasks[0].title == "High priority"


def test_search_by_title_works(tmp_path: Path) -> None:
    _database_path, repository = _create_repository(tmp_path)
    repository.add_task(
        Task(title="Build dark mode", description="", priority="High", status="Todo")
    )
    repository.add_task(
        Task(title="Write docs", description="", priority="Low", status="Done")
    )

    tasks = repository.search_tasks_by_title("dark")

    assert len(tasks) == 1
    assert tasks[0].title == "Build dark mode"


def test_sort_by_created_date_works(tmp_path: Path) -> None:
    _database_path, repository = _create_repository(tmp_path)
    repository.add_task(
        Task(
            title="Older task",
            description="",
            priority="Low",
            status="Todo",
            created_at="2024-01-01 10:00:00",
        )
    )
    repository.add_task(
        Task(
            title="Newer task",
            description="",
            priority="High",
            status="Done",
            created_at="2024-01-02 10:00:00",
        )
    )

    newest_first = repository.get_all_tasks(sort_order="desc")
    oldest_first = repository.get_all_tasks(sort_order="asc")

    assert newest_first[0].title == "Newer task"
    assert oldest_first[0].title == "Older task"
