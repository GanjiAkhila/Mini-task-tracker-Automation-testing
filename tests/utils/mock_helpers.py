from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QMessageBox, QFileDialog

def mock_qt_dialogs():
    """
    Returns a dictionary of patches for common Qt dialogs to prevent 
    blocking the test runner with modal windows.
    """
    patches = {
        "question": patch.object(QMessageBox, "question", return_value=QMessageBox.Yes),
        "information": patch.object(QMessageBox, "information"),
        "warning": patch.object(QMessageBox, "warning"),
        "critical": patch.object(QMessageBox, "critical"),
        "getSaveFileName": patch.object(QFileDialog, "getSaveFileName", return_value=("test_export.csv", "CSV Files (*.csv)")),
        "getOpenFileName": patch.object(QFileDialog, "getOpenFileName", return_value=("test_import.csv", "CSV Files (*.csv)")),
    }
    return patches
