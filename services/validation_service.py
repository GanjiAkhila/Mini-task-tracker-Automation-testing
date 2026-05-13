class ValidationService:
    _INVALID_PRIORITY_VALUES = {"", "Select priority"}
    _INVALID_STATUS_VALUES = {"", "Select status"}

    def validate_task(self, title: str, priority: str, status: str) -> list[str]:
        errors: list[str] = []

        if not title.strip():
            errors.append("Title cannot be empty.")
        if priority.strip() in self._INVALID_PRIORITY_VALUES:
            errors.append("Priority must be selected.")
        if status.strip() in self._INVALID_STATUS_VALUES:
            errors.append("Status must be selected.")

        return errors
