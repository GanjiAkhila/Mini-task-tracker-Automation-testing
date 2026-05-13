APP_STYLESHEET = """
QWidget {
    background-color: #101726;
    color: #e6edf7;
    font-family: "DejaVu Sans";
    font-size: 13px;
}

QWidget#mainContainer {
    background-color: #101726;
}

QScrollArea#mainScrollArea {
    border: none;
    background-color: #101726;
}

QFrame#headerCard {
    background-color: #152238;
    border: 1px solid #223552;
    border-radius: 18px;
}

QFrame#formCard,
QFrame#filterCard,
QFrame#tableCard,
QFrame#actionCard,
QFrame#summaryCard {
    background-color: #162134;
    border: 1px solid #24334c;
    border-radius: 16px;
}

QFrame#summaryCard[accent="total"] {
    border-top: 4px solid #4ea4ff;
}

QFrame#summaryCard[accent="todo"] {
    border-top: 4px solid #f2b94b;
}

QFrame#summaryCard[accent="in_progress"] {
    border-top: 4px solid #62a7ff;
}

QFrame#summaryCard[accent="done"] {
    border-top: 4px solid #37d39a;
}

QFrame#summaryCard[accent="high_priority"] {
    border-top: 4px solid #f06b7d;
}

QLabel#headerTitle {
    color: #f8fbff;
    font-size: 28px;
    font-weight: 700;
}

QLabel#headerSubtitle {
    color: #9eb2cc;
    font-size: 14px;
}

QLabel#cardTitle {
    color: #f6faff;
    font-size: 17px;
    font-weight: 700;
}

QLabel#cardSubtitle {
    color: #8ea4c1;
    font-size: 12px;
}

QLabel#sectionLabel {
    color: #d5e4f8;
    font-size: 13px;
    font-weight: 600;
}

QLabel#fieldLabel {
    color: #a4bbd7;
    font-size: 12px;
    font-weight: 600;
}

QLabel#summaryCardTitle {
    color: #93aac7;
    font-size: 12px;
    font-weight: 600;
}

QLabel#summaryCardValue {
    color: #f9fbff;
    font-size: 26px;
    font-weight: 700;
}

QLabel#emptyStateLabel {
    color: #9bb0cb;
    background-color: #101a29;
    border: 1px dashed #324867;
    border-radius: 12px;
    padding: 14px;
}

QLineEdit,
QTextEdit,
QComboBox,
QTableWidget {
    background-color: #0f1725;
    border: 1px solid #2a3a56;
    border-radius: 10px;
    color: #edf4ff;
}

QLineEdit,
QComboBox {
    padding: 0 12px;
}

QComboBox {
    padding-right: 28px;
}

QTextEdit {
    padding: 10px 12px;
}

QTextEdit {
    min-height: 140px;
}

QLineEdit:focus,
QTextEdit:focus,
QComboBox:focus,
QTableWidget:focus {
    border: 1px solid #4f95ff;
}

QComboBox::drop-down {
    border: none;
    width: 28px;
}

QPushButton {
    min-height: 42px;
    padding: 0 18px;
    border-radius: 10px;
    border: 1px solid transparent;
    font-weight: 600;
}

QPushButton#primaryButton {
    background-color: #2877ff;
    color: #ffffff;
}

QPushButton#primaryButton:hover {
    background-color: #3d87ff;
}

QPushButton#primaryButton:pressed {
    background-color: #1f67df;
}

QPushButton#dangerButton {
    background-color: #d14b5f;
    color: #ffffff;
}

QPushButton#dangerButton:hover {
    background-color: #df6074;
}

QPushButton#dangerButton:pressed {
    background-color: #b63f52;
}

QPushButton#neutralButton {
    background-color: #223149;
    border: 1px solid #344968;
    color: #edf4ff;
}

QPushButton#neutralButton:hover {
    background-color: #2b3d59;
}

QPushButton#neutralButton:pressed {
    background-color: #1d2c43;
}

QSplitter::handle {
    background-color: transparent;
}

QSplitter::handle:horizontal {
    width: 10px;
}

QHeaderView::section {
    background-color: #1d2b42;
    color: #eff6ff;
    border: none;
    border-bottom: 1px solid #314564;
    padding: 12px 10px;
    font-weight: 700;
}

QTableWidget {
    gridline-color: #23354d;
    selection-background-color: #23406b;
    selection-color: #ffffff;
    alternate-background-color: #132033;
}

QTableWidget::item {
    padding: 10px;
    border: none;
}

QTableCornerButton::section {
    background-color: #1d2b42;
    border: none;
}

QScrollBar:vertical {
    background: #101726;
    width: 12px;
    margin: 8px 0 8px 0;
}

QScrollBar::handle:vertical {
    background: #314664;
    border-radius: 6px;
    min-height: 28px;
}

QScrollBar:horizontal {
    background: #101726;
    height: 12px;
    margin: 0 8px 0 8px;
}

QScrollBar::handle:horizontal {
    background: #314664;
    border-radius: 6px;
    min-width: 28px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical,
QScrollBar:horizontal,
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
    border: none;
}

QStatusBar#appStatusBar {
    background-color: #0d1420;
    color: #9eb2cc;
    border-top: 1px solid #1f2f48;
}

QStatusBar::item {
    border: none;
}
"""
