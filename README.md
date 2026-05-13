# Mini Task Tracker

## Problem Statement

Mini Task Tracker is a small Linux desktop application for managing software development tasks locally. It allows users to add, view, edit, delete, search, and filter tasks while storing all data in SQLite. The project follows a strict MVC structure so the UI, controller logic, persistence layer, and validation rules remain separated and easy to maintain.

## Features

- Add tasks with title, description, priority, and status
- View all tasks in a table
- Edit a selected task
- Delete a selected task with confirmation
- Search tasks by title
- Filter tasks by status and priority
- Persist task data locally with SQLite
- Validate required fields before saving
- Keep UI, business flow, validation, and database logic separated with MVC

## Tech Stack

- Python
- PySide6
- SQLite
- Pytest

## Folder Structure

```text
mini_task_tracker/
├── main.py
├── requirements.txt
├── README.md
├── models/
│   └── task.py
├── views/
│   ├── main_window.py
│   └── task_form.py
├── controllers/
│   └── task_controller.py
├── repositories/
│   └── task_repository.py
├── services/
│   └── validation_service.py
├── tests/
│   └── test_validation_service.py
└── docs/
    ├── AI_USAGE_LOG.md
    ├── PROMPTS.md
    └── FINAL_REFLECTION.md
```

## How to Install Dependencies

```bash
pip install -r requirements.txt
```

## How to Run the App

```bash
python main.py
```

## How to Run Tests

```bash
pytest
```

## MVC Explanation

- Model
  `models/task.py` contains the `Task` dataclass only. It represents the task data structure and has no UI or database logic.

- View
  `views/task_form.py` and `views/main_window.py` contain only PySide6 widgets, layouts, dialogs, and helper methods for presenting data. The views do not talk to SQLite and do not perform validation.

- Controller
  `controllers/task_controller.py` handles user actions and coordinates the view, repository, and validation service. It owns add, edit, delete, refresh, search, and filter behavior.

- Repository
  `repositories/task_repository.py` is responsible for SQLite access only. It creates the table on startup and provides CRUD, search, and filter methods.

- Service
  `services/validation_service.py` contains only validation rules and returns clear error messages for invalid input.
