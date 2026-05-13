from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)

from models.task import Task


class TaskForm(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        self.setObjectName("taskForm")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title")
        self.title_input.setMinimumHeight(44)
        self.title_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter task description")
        self.description_input.setMinimumHeight(120)
        self.description_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.priority_input = QComboBox()
        self.priority_input.addItem("Select priority", "")
        self.priority_input.addItems(["Low", "Medium", "High"])
        self.priority_input.setMinimumHeight(44)
        self.priority_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.status_input = QComboBox()
        self.status_input.addItem("Select status", "")
        self.status_input.addItems(["Todo", "In Progress", "Done"])
        self.status_input.setMinimumHeight(44)
        self.status_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.submit_button = QPushButton("+ Add Task")
        self.submit_button.setObjectName("primaryButton")
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("neutralButton")

        title_label = QLabel("Title")
        title_label.setObjectName("fieldLabel")

        description_label = QLabel("Description")
        description_label.setObjectName("fieldLabel")

        priority_label = QLabel("Priority")
        priority_label.setObjectName("fieldLabel")

        status_label = QLabel("Status")
        status_label.setObjectName("fieldLabel")

        field_row = QHBoxLayout()
        field_row.setSpacing(16)

        priority_layout = QVBoxLayout()
        priority_layout.setSpacing(8)
        priority_layout.addWidget(priority_label)
        priority_layout.addWidget(self.priority_input)

        status_layout = QVBoxLayout()
        status_layout.setSpacing(8)
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_input)

        field_row.addLayout(priority_layout, 1)
        field_row.addLayout(status_layout, 1)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.title_input)
        main_layout.addSpacing(4)
        main_layout.addWidget(description_label)
        main_layout.addWidget(self.description_input, 1)
        main_layout.addSpacing(4)
        main_layout.addLayout(field_row)
        main_layout.addSpacing(8)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def get_form_data(self) -> dict[str, str]:
        return {
            "title": self.title_input.text().strip(),
            "description": self.description_input.toPlainText().strip(),
            "priority": self.priority_input.currentText()
            if self.priority_input.currentIndex() > 0
            else "",
            "status": self.status_input.currentText()
            if self.status_input.currentIndex() > 0
            else "",
        }

    def set_task(self, task: Task) -> None:
        self.title_input.setText(task.title)
        self.description_input.setPlainText(task.description)
        self._set_combo_value(self.priority_input, task.priority)
        self._set_combo_value(self.status_input, task.status)

    def clear_form(self) -> None:
        self.title_input.clear()
        self.description_input.clear()
        self.priority_input.setCurrentIndex(0)
        self.status_input.setCurrentIndex(0)
        self.title_input.setFocus()

    def set_edit_mode(self, is_editing: bool) -> None:
        self.submit_button.setText("Update Task" if is_editing else "+ Add Task")

    @staticmethod
    def _set_combo_value(combo_box: QComboBox, value: str) -> None:
        index = combo_box.findText(value)
        combo_box.setCurrentIndex(index if index >= 0 else 0)
