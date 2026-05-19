from dataclasses import dataclass


@dataclass
class Task:
    id: int | None = None
    title: str = ""
    description: str = ""
    priority: str = ""
    status: str = ""
    created_at: str = ""
    deleted_at: str | None = None
