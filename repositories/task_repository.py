import sqlite3
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

from models.task import Task


class TaskRepository:
    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self._create_table()
        self._ensure_schema()

    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_table(self) -> None:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            deleted_at TEXT
        )
        """
        with self._get_connection() as connection:
            connection.execute(create_table_query)
            connection.commit()

    def _ensure_schema(self) -> None:
        with self._get_connection() as connection:
            columns = {
                row["name"] for row in connection.execute("PRAGMA table_info(tasks)")
            }
            if "deleted_at" not in columns:
                connection.execute("ALTER TABLE tasks ADD COLUMN deleted_at TEXT")
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_tasks_deleted_at ON tasks(deleted_at)"
            )
            connection.commit()

    def add_task(self, task: Task) -> int:
        created_at = task.created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_query = """
        INSERT INTO tasks (title, description, priority, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        with self._get_connection() as connection:
            cursor = connection.execute(
                insert_query,
                (
                    task.title,
                    task.description,
                    task.priority,
                    task.status,
                    created_at,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def update_task(self, task: Task) -> None:
        update_query = """
        UPDATE tasks
        SET title = ?, description = ?, priority = ?, status = ?
        WHERE id = ?
        """
        with self._get_connection() as connection:
            connection.execute(
                update_query,
                (
                    task.title,
                    task.description,
                    task.priority,
                    task.status,
                    task.id,
                ),
            )
            connection.commit()

    def delete_task(self, task_id: int) -> None:
        deleted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        delete_query = "UPDATE tasks SET deleted_at = ? WHERE id = ?"
        with self._get_connection() as connection:
            connection.execute(delete_query, (deleted_at, task_id))
            connection.commit()

    def restore_task(self, task_id: int) -> None:
        restore_query = "UPDATE tasks SET deleted_at = NULL WHERE id = ?"
        with self._get_connection() as connection:
            connection.execute(restore_query, (task_id,))
            connection.commit()

    def delete_task_permanently(self, task_id: int) -> None:
        delete_query = "DELETE FROM tasks WHERE id = ?"
        with self._get_connection() as connection:
            connection.execute(delete_query, (task_id,))
            connection.commit()

    def empty_recycle_bin(self) -> None:
        delete_query = "DELETE FROM tasks WHERE deleted_at IS NOT NULL"
        with self._get_connection() as connection:
            connection.execute(delete_query)
            connection.commit()

    def get_all_tasks(
        self, sort_order: str = "desc", include_deleted: bool = False
    ) -> list[Task]:
        query = "SELECT * FROM tasks"
        if not include_deleted:
            query += " WHERE deleted_at IS NULL"
        query += f" ORDER BY {self._build_order_by(sort_order)}"
        return self._fetch_many(query)

    def get_deleted_tasks(self, sort_order: str = "desc") -> list[Task]:
        query = (
            "SELECT * FROM tasks WHERE deleted_at IS NOT NULL "
            f"ORDER BY {self._build_deleted_order_by(sort_order)}"
        )
        return self._fetch_many(query)

    def get_task_by_id(
        self, task_id: int, include_deleted: bool = False
    ) -> Task | None:
        query = "SELECT * FROM tasks WHERE id = ?"
        parameters: tuple[object, ...] = (task_id,)
        if not include_deleted:
            query += " AND deleted_at IS NULL"
        with self._get_connection() as connection:
            row = connection.execute(query, parameters).fetchone()
        return self._row_to_task(row) if row else None

    def search_tasks_by_title(
        self, title_query: str, sort_order: str = "desc"
    ) -> list[Task]:
        query = (
            "SELECT * FROM tasks WHERE deleted_at IS NULL AND LOWER(title) LIKE LOWER(?) "
            f"ORDER BY {self._build_order_by(sort_order)}"
        )
        return self._fetch_many(query, (f"%{title_query}%",))

    def filter_tasks(
        self,
        status: str = "",
        priority: str = "",
        sort_order: str = "desc",
    ) -> list[Task]:
        query = "SELECT * FROM tasks WHERE deleted_at IS NULL"
        parameters: list[str] = []

        if status:
            query += " AND status = ?"
            parameters.append(status)
        if priority:
            query += " AND priority = ?"
            parameters.append(priority)

        query += f" ORDER BY {self._build_order_by(sort_order)}"
        return self._fetch_many(query, tuple(parameters))

    def query_tasks(
        self,
        status: str = "",
        priority: str = "",
        title_query: str = "",
        sort_order: str = "desc",
    ) -> list[Task]:
        query = "SELECT * FROM tasks WHERE deleted_at IS NULL"
        parameters: list[str] = []

        if status:
            query += " AND status = ?"
            parameters.append(status)
        if priority:
            query += " AND priority = ?"
            parameters.append(priority)
        if title_query:
            query += " AND LOWER(title) LIKE LOWER(?)"
            parameters.append(f"%{title_query}%")

        query += f" ORDER BY {self._build_order_by(sort_order)}"
        return self._fetch_many(query, tuple(parameters))

    def _fetch_many(
        self, query: str, parameters: Sequence[object] = ()
    ) -> list[Task]:
        with self._get_connection() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [self._row_to_task(row) for row in rows]

    @staticmethod
    def _build_order_by(sort_order: str) -> str:
        if sort_order == "asc":
            return "created_at ASC, id ASC"
        return "created_at DESC, id DESC"

    @staticmethod
    def _build_deleted_order_by(sort_order: str) -> str:
        if sort_order == "asc":
            return "deleted_at ASC, id ASC"
        return "deleted_at DESC, id DESC"

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> Task:
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"] or "",
            priority=row["priority"],
            status=row["status"],
            created_at=row["created_at"],
            deleted_at=row["deleted_at"] if "deleted_at" in row.keys() else None,
        )
