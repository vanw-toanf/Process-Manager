from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMessageBox

def create_guide_action(parent, callback):
    guide_action = QAction('&User guide. (Ctrl+H)', parent)
    guide_action.setShortcut('Ctrl+H')
    guide_action.triggered.connect(callback)
    return guide_action

def create_about_action(parent, callback):
    about_action = QAction('&Information', parent)
    about_action.triggered.connect(callback)
    return about_action

def show_guide_dialog(parent_window):
    guide_text = """
    <b>Task Manager User Guide:</b>
    <br><br>
    - <b>W</b>: Move selection up in the process list.
    <br>
    - <b>S</b>: Move selection down in the process list.
    <br>
    - <b>Q</b>: Terminate the selected process (confirmation will be required).
    <br>
    - <b>ESC</b>: Exit the application.
    <br>
    - <b>Click on a column header</b>: Sort processes by that column.
    <br>
    - <b>Help Menu -> User Guide (Ctrl+H)</b>: Display this guide.
    <br><br>
    <i>Note: To terminate some system or other users' processes, 
    you may need to run this application with administrative privileges (sudo).</i>
    """
    QMessageBox.information(parent_window, "User Guide", guide_text)

def show_about_dialog(parent_window):
    about_text = """
    <b>Ubuntu Task Manager</b>
    <br><br>
    Built with Python, PyQt6, and psutil.
    <br>
    A simple application for monitoring and managing processes on Ubuntu.
    """
    QMessageBox.about(parent_window, "Information", about_text)