import csv
from pathlib import Path

from models.task import Task


class CSVExportService:
    def export_tasks(self, tasks: list[Task], file_path: str | Path) -> None:
        path = Path(file_path)
        if path.suffix.lower() != ".csv":
            path = path.with_suffix(".csv")

        with path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ["ID", "Title", "Description", "Priority", "Status", "Created Date"]
            )

            for task in tasks:
                writer.writerow(
                    [
                        task.id,
                        task.title,
                        task.description,
                        task.priority,
                        task.status,
                        task.created_at,
                    ]
                )
