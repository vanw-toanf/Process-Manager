import datetime
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget,
                             QMessageBox, QStatusBar)
from PyQt6.QtCore import QTimer, Qt

from app.core import system_monitor, process_handler
from app.ui.system_info_bar import SystemInfoBar
from app.ui.process_table import ProcessTable
from app.ui import menu_actions

class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ubuntu Task Manager (Ctrl+H to view guide)")
        self.setGeometry(100, 100, 1110, 700)

        # --- Menu Bar ---
        self._setup_menu()

        # --- Central Widget and Layout ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # --- System Info Bar ---
        self.system_info_widget = SystemInfoBar()
        self.main_layout.addWidget(self.system_info_widget)

        # --- Table Widget ---
        self.process_table_widget = ProcessTable()
        self.main_layout.addWidget(self.process_table_widget)

        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # --- Timer ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all_data)
        self.timer.start(2000)  # Update every 2 seconds

        self.refresh_all_data() # Get initial data
        self.process_table_widget.setFocus()

    def _setup_menu(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu('&Help')

        guide_action = menu_actions.create_guide_action(self, self._show_guide)
        help_menu.addAction(guide_action)

        about_action = menu_actions.create_about_action(self, self._show_about)
        help_menu.addAction(about_action)

    def refresh_all_data(self):
        """
        Update both system info and process data.
        """
        self._update_system_info_display()
        self._load_process_data_display()
        self.status_bar.showMessage(f"Last updated: {datetime.datetime.now().strftime('%H:%M:%S')}")

    def _update_system_info_display(self):
        try:
            cpu = system_monitor.get_cpu_usage()
            mem = system_monitor.get_memory_info()
            swap = system_monitor.get_swap_info()
            self.system_info_widget.update_info(cpu, mem, swap)
        except Exception as e:
            self.system_info_widget.update_info("Error", None, None)
            print(f"Error updating system information: {e}")

    def _load_process_data_display(self):
        try:
            processes = process_handler.get_all_processes_info()
            self.process_table_widget.update_data(processes)
        except Exception as e:
            QMessageBox.critical(self, "Error loading processes", f"Unable to load the process list: {e}")
            print(f"Error loading process data: {e}")


    def keyPressEvent(self, event):
        key = event.key()
        table = self.process_table_widget
        current_row = table.currentRow()

        if key == Qt.Key.Key_Escape:
            self.close()
        elif key == Qt.Key.Key_W:
            if current_row > 0:
                table.selectRow(current_row - 1)
            elif table.rowCount() > 0: # Cycle to the last row
                table.selectRow(table.rowCount() - 1)
        elif key == Qt.Key.Key_S:
            if current_row < table.rowCount() - 1:
                table.selectRow(current_row + 1)
            elif table.rowCount() > 0: # Cycle to the first row
                table.selectRow(0)
        elif key == Qt.Key.Key_Q:
            self._terminate_selected_process_ui()
        else:
            super().keyPressEvent(event) # Move to the default key handling

    def _terminate_selected_process_ui(self):
        pid, name = self.process_table_widget.get_selected_pid_and_name()

        if pid is None:
            QMessageBox.warning(self, "No process selected", "Please select a process to terminate.")
            return

        confirm_msg = f"Are you sure you want to terminate the process '{name}' (PID: {pid})?"
        reply = QMessageBox.question(self, 'Confirm process termination',
                                     confirm_msg, QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            success, message = process_handler.terminate_process_by_pid(pid)
            if success:
                QMessageBox.information(self, "Notification", message)
            else:
                QMessageBox.critical(self, "Error", message)
            self._load_process_data_display() # Refresh the process list after termination

    def _show_guide(self):
        menu_actions.show_guide_dialog(self)

    def _show_about(self):
        menu_actions.show_about_dialog(self)