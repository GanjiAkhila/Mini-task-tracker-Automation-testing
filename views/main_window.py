from collections.abc import Mapping, Sequence

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStatusBar,
    QSplitter,
    QStyle,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QComboBox,
)

from models.task import Task
from views.task_form import TaskForm


class SummaryCard(QFrame):
    def __init__(self, title: str, accent: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("summaryCard")
        self.setProperty("accent", accent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("summaryCardTitle")

        self.value_label = QLabel("0")
        self.value_label.setObjectName("summaryCardValue")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value: int) -> None:
        self.value_label.setText(str(value))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Mini Task Tracker")
        self.resize(1280, 860)
        self.setMinimumSize(960, 720)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.is_recycle_bin_mode = False
        self.summary_cards: dict[str, SummaryCard] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setObjectName("mainScrollArea")

        central_widget = QWidget()
        central_widget.setObjectName("mainContainer")
        central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 20)
        main_layout.setSpacing(20)

        main_layout.addWidget(self._build_header_card())
        main_layout.addLayout(self._build_summary_cards())

        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setChildrenCollapsible(False)
        content_splitter.setHandleWidth(10)
        content_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        form_card, form_layout = self._create_card(
            "formCard",
            "Task Form",
            "Create a new task or update the selected one without leaving the screen.",
        )
        self.task_form = TaskForm()
        form_layout.addWidget(self.task_form)
        form_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        content_splitter.addWidget(form_card)

        filter_card, filter_card_layout = self._create_card(
            "filterCard",
            "Search And Filter",
            "Narrow the list quickly using status, priority, or title search.",
        )
        filter_layout = QGridLayout()
        filter_layout.setHorizontalSpacing(12)
        filter_layout.setVerticalSpacing(12)

        self.status_filter = QComboBox()
        self.status_filter.addItem("All Statuses", "")
        self.status_filter.addItems(["Todo", "In Progress", "Done"])
        self.status_filter.setMinimumHeight(42)
        self.status_filter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.priority_filter = QComboBox()
        self.priority_filter.addItem("All Priorities", "")
        self.priority_filter.addItems(["Low", "Medium", "High"])
        self.priority_filter.setMinimumHeight(42)
        self.priority_filter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title")
        self.search_input.setMinimumHeight(42)
        self.search_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.sort_order_combo = QComboBox()
        self.sort_order_combo.addItem("Newest First", "desc")
        self.sort_order_combo.addItem("Oldest First", "asc")
        self.sort_order_combo.setMinimumHeight(42)
        self.sort_order_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.apply_filter_button = QPushButton("Apply Filter")
        self.apply_filter_button.setObjectName("primaryButton")
        self.clear_filter_button = QPushButton("Clear Filter")
        self.clear_filter_button.setObjectName("neutralButton")

        status_label = QLabel("Status")
        status_label.setObjectName("fieldLabel")
        priority_label = QLabel("Priority")
        priority_label.setObjectName("fieldLabel")
        search_label = QLabel("Search Title")
        search_label.setObjectName("fieldLabel")
        sort_label = QLabel("Sort By Created Date")
        sort_label.setObjectName("fieldLabel")

        filter_layout.addWidget(status_label, 0, 0)
        filter_layout.addWidget(priority_label, 0, 1)
        filter_layout.addWidget(self.status_filter, 1, 0)
        filter_layout.addWidget(self.priority_filter, 1, 1)
        filter_layout.addWidget(search_label, 2, 0, 1, 2)
        filter_layout.addWidget(self.search_input, 3, 0, 1, 2)
        filter_layout.addWidget(sort_label, 4, 0, 1, 2)
        filter_layout.addWidget(self.sort_order_combo, 5, 0, 1, 2)
        filter_layout.addWidget(self.apply_filter_button, 6, 0)
        filter_layout.addWidget(self.clear_filter_button, 6, 1)
        filter_layout.setRowStretch(7, 1)
        filter_card_layout.addLayout(filter_layout)
        filter_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        content_splitter.addWidget(filter_card)
        content_splitter.setStretchFactor(0, 3)
        content_splitter.setStretchFactor(1, 2)

        main_layout.addWidget(content_splitter)

        table_card, table_layout = self._create_card(
            "tableCard",
            "Task Table",
            "Browse every task, then select a row to edit or remove it.",
        )
        table_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.empty_state_label = QLabel(
            "No tasks found. Add your first task to get started."
        )
        self.empty_state_label.setObjectName("emptyStateLabel")
        self.empty_state_label.setAlignment(Qt.AlignCenter)
        self.empty_state_label.setWordWrap(True)
        self.empty_state_label.hide()
        table_layout.addWidget(self.empty_state_label)

        self.task_table = QTableWidget(0, 5)
        self.task_table.setObjectName("taskTable")
        self.task_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.task_table.setHorizontalHeaderLabels(
            ["ID", "Title", "Priority", "Status", "Created Date"]
        )
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.task_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.verticalHeader().setDefaultSectionSize(46)
        self.task_table.setAlternatingRowColors(True)
        self.task_table.setShowGrid(True)
        self.task_table.setFocusPolicy(Qt.StrongFocus)
        self.task_table.setCornerButtonEnabled(False)
        self.task_table.setSortingEnabled(False)
        self.task_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.task_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.task_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.task_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        self.task_table.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.ResizeToContents
        )
        self.task_table.horizontalHeader().setDefaultAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )
        table_layout.addWidget(self.task_table, 1)
        main_layout.addWidget(table_card, 1)

        action_card = QFrame()
        action_card.setObjectName("actionCard")
        action_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        action_layout = QHBoxLayout(action_card)
        action_layout.setContentsMargins(18, 16, 18, 16)
        action_layout.setSpacing(12)

        action_label = QLabel("Quick Actions")
        action_label.setObjectName("sectionLabel")
        self.action_hint_label = QLabel(
            "Select a row to edit or delete, or refresh the list."
        )
        self.action_hint_label.setObjectName("cardSubtitle")

        action_title_layout = QVBoxLayout()
        action_title_layout.setSpacing(2)
        action_title_layout.addWidget(action_label)
        action_title_layout.addWidget(self.action_hint_label)

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.setObjectName("neutralButton")
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setObjectName("dangerButton")
        self.restore_button = QPushButton("Restore Selected")
        self.restore_button.setObjectName("neutralButton")
        self.delete_forever_button = QPushButton("Delete Permanently")
        self.delete_forever_button.setObjectName("dangerButton")
        self.empty_bin_button = QPushButton("Empty Recycle Bin")
        self.empty_bin_button.setObjectName("dangerButton")
        self.export_button = QPushButton("Export CSV")
        self.export_button.setObjectName("neutralButton")
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("neutralButton")
        self.recycle_bin_button = QPushButton("Open Recycle Bin")
        self.recycle_bin_button.setObjectName("neutralButton")
        self._set_action_button_icons()

        self.restore_button.hide()
        self.delete_forever_button.hide()
        self.empty_bin_button.hide()

        action_layout.addLayout(action_title_layout)
        action_layout.addStretch()
        action_layout.addWidget(self.edit_button)
        action_layout.addWidget(self.delete_button)
        action_layout.addWidget(self.restore_button)
        action_layout.addWidget(self.delete_forever_button)
        action_layout.addWidget(self.empty_bin_button)
        action_layout.addWidget(self.export_button)
        action_layout.addWidget(self.refresh_button)
        action_layout.addWidget(self.recycle_bin_button)
        main_layout.addWidget(action_card)

        central_widget.setLayout(main_layout)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

        status_bar = QStatusBar(self)
        status_bar.setObjectName("appStatusBar")
        self.setStatusBar(status_bar)

    def populate_tasks(self, tasks: Sequence[Task]) -> None:
        self.task_table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            items = [
                QTableWidgetItem(str(task.id or "")),
                QTableWidgetItem(task.title),
                QTableWidgetItem(task.priority),
                QTableWidgetItem(task.status),
                QTableWidgetItem(
                    task.deleted_at if self.is_recycle_bin_mode else task.created_at
                ),
            ]

            items[0].setTextAlignment(Qt.AlignCenter)
            items[2].setTextAlignment(Qt.AlignCenter)
            items[3].setTextAlignment(Qt.AlignCenter)
            items[4].setTextAlignment(Qt.AlignCenter)

            for column, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.task_table.setItem(row, column, item)

        self.task_table.clearSelection()

    def get_selected_task_id(self) -> int | None:
        selected_items = self.task_table.selectedItems()
        if not selected_items:
            return None

        selected_row = selected_items[0].row()
        item = self.task_table.item(selected_row, 0)
        return int(item.text()) if item and item.text().isdigit() else None

    def get_filter_values(self) -> dict[str, str]:
        return {
            "status": self.status_filter.currentText()
            if self.status_filter.currentIndex() > 0
            else "",
            "priority": self.priority_filter.currentText()
            if self.priority_filter.currentIndex() > 0
            else "",
            "title_query": self.search_input.text().strip(),
            "sort_order": self.sort_order_combo.currentData() or "desc",
        }

    def clear_filters(self) -> None:
        self.status_filter.setCurrentIndex(0)
        self.priority_filter.setCurrentIndex(0)
        self.search_input.clear()

    def set_recycle_bin_mode(self, is_enabled: bool) -> None:
        self.is_recycle_bin_mode = is_enabled
        self.task_form.setEnabled(not is_enabled)
        self.edit_button.setVisible(not is_enabled)
        self.delete_button.setVisible(not is_enabled)
        self.export_button.setVisible(not is_enabled)

        self.restore_button.setVisible(is_enabled)
        self.delete_forever_button.setVisible(is_enabled)
        self.empty_bin_button.setVisible(is_enabled)

        self.recycle_bin_button.setText(
            "Close Recycle Bin" if is_enabled else "Open Recycle Bin"
        )
        self.recycle_bin_button.setIcon(
            self.style().standardIcon(
                QStyle.SP_DialogCloseButton
                if is_enabled
                else QStyle.SP_TrashIcon
            )
        )
        self.task_table.setHorizontalHeaderItem(
            4, QTableWidgetItem("Deleted Date" if is_enabled else "Created Date")
        )
        self.action_hint_label.setText(
            "Restore a deleted task or remove it permanently."
            if is_enabled
            else "Select a row to edit or delete, or refresh the list."
        )

    def update_summary_cards(self, summary: Mapping[str, int]) -> None:
        for key, card in self.summary_cards.items():
            card.set_value(summary.get(key, 0))

    def set_empty_state(self, message: str | None) -> None:
        if message:
            self.empty_state_label.setText(message)
            self.empty_state_label.show()
            return

        self.empty_state_label.hide()

    def show_status_message(self, message: str, timeout_ms: int = 5000) -> None:
        self.statusBar().showMessage(message, timeout_ms)

    def show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Validation Error", message)

    def show_critical(self, title: str, message: str) -> None:
        QMessageBox.critical(self, title, message)

    def show_warning(self, message: str) -> None:
        QMessageBox.warning(self, "Mini Task Tracker", message)

    def prompt_export_file_path(self) -> str:
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Tasks to CSV",
            "mini_task_tracker_tasks.csv",
            "CSV Files (*.csv)",
        )
        return file_path

    def ask_delete_confirmation(self, task_title: str) -> bool:
        answer = QMessageBox.question(
            self,
            "Move To Recycle Bin",
            f"Move the selected task to recycle bin?\n\n{task_title}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return answer == QMessageBox.Yes

    def ask_permanent_delete_confirmation(self, task_title: str) -> bool:
        answer = QMessageBox.question(
            self,
            "Permanent Delete",
            (
                "Permanently delete this task?\n\n"
                f"{task_title}\n\nThis action cannot be undone."
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return answer == QMessageBox.Yes

    def ask_empty_recycle_bin_confirmation(self, deleted_count: int) -> bool:
        answer = QMessageBox.question(
            self,
            "Empty Recycle Bin",
            (
                f"Permanently delete {deleted_count} task(s) from recycle bin?\n\n"
                "This action cannot be undone."
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return answer == QMessageBox.Yes

    def _build_header_card(self) -> QFrame:
        header_card = QFrame()
        header_card.setObjectName("headerCard")

        layout = QVBoxLayout(header_card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(6)

        title_label = QLabel("Mini Task Tracker")
        title_label.setObjectName("headerTitle")

        subtitle_label = QLabel(
            "Track, organize, and complete your development tasks efficiently."
        )
        subtitle_label.setObjectName("headerSubtitle")
        subtitle_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        return header_card

    def _set_action_button_icons(self) -> None:
        icon_size = QSize(18, 18)

        self.delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.delete_button.setIconSize(icon_size)

        self.refresh_button.setIcon(
            self.style().standardIcon(QStyle.SP_BrowserReload)
        )
        self.refresh_button.setIconSize(icon_size)

        self.recycle_bin_button.setIcon(
            self.style().standardIcon(QStyle.SP_TrashIcon)
        )
        self.recycle_bin_button.setIconSize(icon_size)

    def _build_summary_cards(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(16)

        card_definitions = [
            ("Total Tasks", "total"),
            ("Todo", "todo"),
            ("In Progress", "in_progress"),
            ("Done", "done"),
            ("High Priority", "high_priority"),
        ]

        for title, key in card_definitions:
            card = SummaryCard(title, key)
            self.summary_cards[key] = card
            layout.addWidget(card, 1)

        return layout

    def _create_card(
        self, object_name: str, title: str, subtitle: str
    ) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setObjectName(object_name)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 20)
        layout.setSpacing(14)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        layout.addWidget(title_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("cardSubtitle")
        subtitle_label.setWordWrap(True)
        layout.addWidget(subtitle_label)

        return card, layout
