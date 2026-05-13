import sqlite3
import pytest
from models.task import Task
from repositories.task_repository import TaskRepository

def test_repository_initialization_creates_table(db_path):
    # Initialize the repository to trigger table creation
    repo = TaskRepository(db_path)
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'"
        )
        assert cursor.fetchone() is not None

def test_add_task_returns_id(repository):
    task = Task(title="Test", priority="High", status="Todo")
    task_id = repository.add_task(task)
    assert isinstance(task_id, int)
    assert task_id > 0

def test_get_task_by_id(repository):
    task = Task(title="Get Me", priority="Low", status="Done")
    task_id = repository.add_task(task)
    
    fetched = repository.get_task_by_id(task_id)
    assert fetched is not None
    assert fetched.id == task_id
    assert fetched.title == "Get Me"

def test_get_task_by_id_not_found(repository):
    assert repository.get_task_by_id(999) is None

def test_get_all_tasks_sorting(repository):
    repository.add_task(Task(title="Old", priority="Low", status="Todo", created_at="2020-01-01 10:00:00"))
    repository.add_task(Task(title="New", priority="High", status="Done", created_at="2026-01-01 10:00:00"))
    
    # Newest first (default)
    tasks = repository.get_all_tasks(sort_order="desc")
    assert tasks[0].title == "New"
    
    # Oldest first
    tasks = repository.get_all_tasks(sort_order="asc")
    assert tasks[0].title == "Old"

def test_update_task(repository):
    task_id = repository.add_task(Task(title="Before", priority="Low", status="Todo"))
    
    updated_task = Task(
        id=task_id,
        title="After",
        description="Updated",
        priority="High",
        status="Done"
    )
    repository.update_task(updated_task)
    
    fetched = repository.get_task_by_id(task_id)
    assert fetched.title == "After"
    assert fetched.description == "Updated"
    assert fetched.priority == "High"
    assert fetched.status == "Done"

def test_delete_task(repository):
    task_id = repository.add_task(Task(title="Delete", priority="Low", status="Todo"))
    assert repository.get_task_by_id(task_id) is not None
    
    repository.delete_task(task_id)
    assert repository.get_task_by_id(task_id) is None

def test_search_tasks_by_title_case_insensitive(repository):
    repository.add_task(Task(title="Python Task", priority="High", status="Todo"))
    repository.add_task(Task(title="JavaScript Task", priority="Low", status="Todo"))
    
    # Case insensitive search
    results = repository.search_tasks_by_title("python")
    assert len(results) == 1
    assert results[0].title == "Python Task"

def test_query_tasks_multi_filter(repository):
    repository.add_task(Task(title="Task 1", priority="High", status="Todo"))
    repository.add_task(Task(title="Task 2", priority="Low", status="Todo"))
    repository.add_task(Task(title="Task 3", priority="High", status="Done"))
    
    # Filter by priority AND status
    results = repository.query_tasks(priority="High", status="Todo")
    assert len(results) == 1
    assert results[0].title == "Task 1"

def test_query_tasks_with_title_search(repository):
    repository.add_task(Task(title="Clean Room", priority="High", status="Todo"))
    repository.add_task(Task(title="Clean Car", priority="Low", status="Done"))
    
    results = repository.query_tasks(title_query="room")
    assert len(results) == 1
    assert results[0].title == "Clean Room"

def test_filter_tasks_method(repository):
    # Testing the explicit filter_tasks method used in some parts of the code
    repository.add_task(Task(title="T1", priority="High", status="Todo"))
    repository.add_task(Task(title="T2", priority="Medium", status="Todo"))
    
    results = repository.filter_tasks(priority="High")
    assert len(results) == 1
    assert results[0].title == "T1"

def test_row_to_task_conversion_with_empty_description(repository):
    # Ensure description is converted to "" if NULL in DB
    with sqlite3.connect(repository.database_path) as conn:
        conn.execute(
            "INSERT INTO tasks (title, description, priority, status, created_at) VALUES (?, ?, ?, ?, ?)",
            ("No Desc", None, "Low", "Todo", "2024-01-01 00:00:00")
        )
    
    task = repository.search_tasks_by_title("No Desc")[0]
    assert task.description == ""
