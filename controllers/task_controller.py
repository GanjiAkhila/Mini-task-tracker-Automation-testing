from services.csv_export_service import CSVExportService
from models.task import Task
from repositories.task_repository import TaskRepository
from services.validation_service import ValidationService
from views.main_window import MainWindow


class TaskController:
    def __init__(
        self,
        view: MainWindow,
        repository: TaskRepository,
        validation_service: ValidationService,
        csv_export_service: CSVExportService | None = None,
    ) -> None:
        self.view = view
        self.repository = repository
        self.validation_service = validation_service
        self.csv_export_service = csv_export_service or CSVExportService()
        self.editing_task_id: int | None = None

        self._connect_signals()
        self._refresh_task_table("Ready")

    def _connect_signals(self) -> None:
        self.view.task_form.submit_button.clicked.connect(self.add_task)
        self.view.task_form.clear_button.clicked.connect(self.clear_form)
        self.view.edit_button.clicked.connect(self.edit_selected_task)
        self.view.delete_button.clicked.connect(self.delete_selected_task)
        self.view.refresh_button.clicked.connect(self.refresh_tasks)
        self.view.export_button.clicked.connect(self.export_tasks_to_csv)
        self.view.apply_filter_button.clicked.connect(self.apply_filters)
        self.view.clear_filter_button.clicked.connect(self.clear_filters)
        self.view.sort_order_combo.currentIndexChanged.connect(self.update_sort_order)
        self.view.search_input.returnPressed.connect(self.apply_filters)

    def add_task(self) -> None:
        form_data = self.view.task_form.get_form_data()
        errors = self.validation_service.validate_task(
            title=form_data["title"],
            priority=form_data["priority"],
            status=form_data["status"],
        )

        if errors:
            self.view.show_error("\n".join(errors))
            return

        success_message = "Task added successfully"
        if self.editing_task_id is None:
            task = Task(
                title=form_data["title"],
                description=form_data["description"],
                priority=form_data["priority"],
                status=form_data["status"],
            )
            self.repository.add_task(task)
        else:
            existing_task = self.repository.get_task_by_id(self.editing_task_id)
            if existing_task is None:
                self.view.show_warning("The selected task could not be found.")
                self.reset_form_state()
                self._refresh_task_table("Showing all tasks")
                return

            updated_task = Task(
                id=self.editing_task_id,
                title=form_data["title"],
                description=form_data["description"],
                priority=form_data["priority"],
                status=form_data["status"],
                created_at=existing_task.created_at,
            )
            self.repository.update_task(updated_task)
            success_message = "Task updated successfully"

        self.reset_form_state()
        self._refresh_task_table(success_message)

    def edit_selected_task(self) -> None:
        task_id = self.view.get_selected_task_id()
        if task_id is None:
            self.view.show_status_message("Please select a task first")
            return

        task = self.repository.get_task_by_id(task_id)
        if task is None:
            self.view.show_warning("The selected task could not be found.")
            self._refresh_task_table("Showing all tasks")
            return

        self.editing_task_id = task.id
        self.view.task_form.set_task(task)
        self.view.task_form.set_edit_mode(True)
        self.view.show_status_message("Task loaded for editing")

    def delete_selected_task(self) -> None:
        task_id = self.view.get_selected_task_id()
        if task_id is None:
            self.view.show_status_message("Please select a task first")
            return

        task = self.repository.get_task_by_id(task_id)
        if task is None:
            self.view.show_warning("The selected task could not be found.")
            self._refresh_task_table("Showing all tasks")
            return

        if not self.view.ask_delete_confirmation(task.title):
            return

        self.repository.delete_task(task_id)
        if self.editing_task_id == task_id:
            self.reset_form_state()
        self._refresh_task_table("Task deleted successfully")

    def refresh_tasks(self) -> None:
        status_message = (
            "Filter applied" if self._has_active_filters() else "Showing all tasks"
        )
        self._refresh_task_table(status_message)

    def apply_filters(self) -> None:
        status_message = (
            "Filter applied" if self._has_active_filters() else "Showing all tasks"
        )
        self._refresh_task_table(status_message)

    def clear_filters(self) -> None:
        self.view.clear_filters()
        self._refresh_task_table("Showing all tasks")

    def clear_form(self) -> None:
        self.reset_form_state()
        self.view.show_status_message("Form cleared")

    def export_tasks_to_csv(self) -> None:
        file_path = self.view.prompt_export_file_path()
        if not file_path:
            self.view.show_status_message("Export cancelled")
            return

        try:
            tasks = self.repository.get_all_tasks(self._get_sort_order())
            self.csv_export_service.export_tasks(tasks, file_path)
        except OSError as error:
            self.view.show_critical(
                "Export Failed", f"Could not export tasks.\n\n{error}"
            )
            return

        self.view.show_status_message("Tasks exported successfully.")

    def update_sort_order(self) -> None:
        self._refresh_task_table("Sort order updated")

    def reset_form_state(self) -> None:
        self.editing_task_id = None
        self.view.task_form.clear_form()
        self.view.task_form.set_edit_mode(False)

    def _refresh_task_table(self, status_message: str) -> None:
        filters = self.view.get_filter_values()
        tasks = self.repository.query_tasks(
            status=filters["status"],
            priority=filters["priority"],
            title_query=filters["title_query"],
            sort_order=filters["sort_order"],
        )
        self.view.populate_tasks(tasks)
        self.view.set_empty_state(self._get_empty_state_message(tasks, filters))
        self.view.update_summary_cards(self._build_summary_counts())
        timeout_ms = 0 if status_message == "Ready" else 5000
        self.view.show_status_message(status_message, timeout_ms)

    def _build_summary_counts(self) -> dict[str, int]:
        all_tasks = self.repository.get_all_tasks()
        summary = {
            "total": len(all_tasks),
            "todo": 0,
            "in_progress": 0,
            "done": 0,
            "high_priority": 0,
        }

        for task in all_tasks:
            if task.status == "Todo":
                summary["todo"] += 1
            elif task.status == "In Progress":
                summary["in_progress"] += 1
            elif task.status == "Done":
                summary["done"] += 1

            if task.priority == "High":
                summary["high_priority"] += 1

        return summary

    @staticmethod
    def _get_empty_state_message(tasks: list[Task], filters: dict[str, str]) -> str | None:
        if tasks:
            return None

        if filters["status"] or filters["priority"] or filters["title_query"]:
            return "No matching tasks found. Try changing your filters."

        return "No tasks found. Add your first task to get started."

    def _has_active_filters(self) -> bool:
        filters = self.view.get_filter_values()
        return bool(filters["status"] or filters["priority"] or filters["title_query"])

    def _get_sort_order(self) -> str:
        return self.view.get_filter_values()["sort_order"]
