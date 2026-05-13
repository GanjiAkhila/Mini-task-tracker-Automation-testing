# AI Usage Log

## Session 1

Date: 2026-05-09
Agent Used: Codex (GPT-5 based coding agent)
Task Given: Build a complete Linux desktop task tracker using Python, PySide6, SQLite, and MVC.
Prompt Summary: Create a runnable PySide6 app with add, edit, delete, search, and filter features; use SQLite for persistence; keep model, view, controller, repository, and validation logic cleanly separated; add tests and project documentation.
Files Created/Modified:
- `main.py`
- `requirements.txt`
- `README.md`
- `models/task.py`
- `views/main_window.py`
- `views/task_form.py`
- `controllers/task_controller.py`
- `repositories/task_repository.py`
- `services/validation_service.py`
- `tests/test_validation_service.py`
- `docs/AI_USAGE_LOG.md`
- `docs/PROMPTS.md`
- `docs/FINAL_REFLECTION.md`
What AI Generated: Initial full project scaffold, MVC implementation, SQLite repository layer, PySide6 views, controller flow, validation service, tests, and documentation drafts.
Human Review Notes: Review import paths, verify Qt widget behavior on Linux, and confirm the project runs after installing dependencies.
Issues Found: No functional issues found during the static review; runtime verification still depends on local PySide6 availability.
Follow-up Prompt: Review the generated code, confirm MVC boundaries, and suggest UX polish or extra tests if needed.
Accepted / Rejected / Reworked: Reworked after review and verification pass.
