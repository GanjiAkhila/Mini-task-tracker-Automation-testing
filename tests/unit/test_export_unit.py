import csv
import pytest
from pathlib import Path
from models.task import Task
from services.csv_export_service import CSVExportService

@pytest.fixture
def export_service():
    return CSVExportService()

def test_export_tasks_successful_write(tmp_path, export_service):
    file_path = tmp_path / "tasks.csv"
    tasks = [
        Task(id=1, title="T1", description="D1", priority="High", status="Todo", created_at="2024-01-01"),
        Task(id=2, title="T2", description="D2", priority="Low", status="Done", created_at="2024-01-02")
    ]
    
    export_service.export_tasks(tasks, file_path)
    
    assert file_path.exists()
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        
    assert len(rows) == 3 # Header + 2 tasks
    assert rows[0] == ["ID", "Title", "Description", "Priority", "Status", "Created Date"]
    assert rows[1] == ["1", "T1", "D1", "High", "Todo", "2024-01-01"]
    assert rows[2] == ["2", "T2", "D2", "Low", "Done", "2024-01-02"]

def test_export_tasks_appends_extension(tmp_path, export_service):
    file_path = tmp_path / "my_export"
    export_service.export_tasks([], file_path)
    
    expected_path = tmp_path / "my_export.csv"
    assert expected_path.exists()

def test_export_tasks_handles_path_object(tmp_path, export_service):
    file_path = Path(tmp_path) / "path_test.csv"
    export_service.export_tasks([], file_path)
    assert file_path.exists()

def test_export_empty_list(tmp_path, export_service):
    file_path = tmp_path / "empty.csv"
    export_service.export_tasks([], file_path)
    
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    assert len(rows) == 1 # Only header
    assert rows[0] == ["ID", "Title", "Description", "Priority", "Status", "Created Date"]

def test_export_tasks_encoding(tmp_path, export_service):
    # Test with special characters
    file_path = tmp_path / "special.csv"
    tasks = [Task(id=1, title="Task with 🚀", description="Special chars: ñ, ü, ö", priority="Med", status="Todo")]
    
    export_service.export_tasks(tasks, file_path)
    
    with open(file_path, newline="", encoding="utf-8") as f:
        content = f.read()
        assert "🚀" in content
        assert "ñ, ü, ö" in content
