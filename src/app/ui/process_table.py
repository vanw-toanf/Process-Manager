from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt

class ProcessTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.column_headers = ["PID", "Name", "User", "Status", "CPU %", "RAM (MB)", "Num_threads", "Create_at"]
        self.setColumnCount(len(self.column_headers))
        self.setHorizontalHeaderLabels(self.column_headers)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

    def update_data(self, processes_data):
        current_selected_row = -1
        selected_items = self.selectedItems()
        if selected_items:
            current_selected_row = self.row(selected_items[0])

        sort_column = self.horizontalHeader().sortIndicatorSection()
        sort_order = self.horizontalHeader().sortIndicatorOrder()

        self.setSortingEnabled(False)
        self.setRowCount(0) 
        self.setRowCount(len(processes_data))

        for row_num, p_data in enumerate(processes_data):
            self.setItem(row_num, 0, QTableWidgetItem(str(p_data.get('pid', 'N/A'))))
            self.setItem(row_num, 1, QTableWidgetItem(p_data.get('name', 'N/A')))
            self.setItem(row_num, 2, QTableWidgetItem(p_data.get('username', 'N/A')))
            self.setItem(row_num, 3, QTableWidgetItem(str(p_data.get('status', 'N/A'))))

            cpu_val = p_data.get('cpu_percent', 0.0)
            cpu_item = QTableWidgetItem()
            cpu_item.setData(Qt.ItemDataRole.EditRole, cpu_val) # To ensure sorting 
            self.setItem(row_num, 4, cpu_item)

            memory_val = p_data.get('memory_rss_mb', 0.0)
            memory_item = QTableWidgetItem()
            memory_item.setData(Qt.ItemDataRole.EditRole, memory_val) # To ensure sorting
            self.setItem(row_num, 5, memory_item)

            threads_val = p_data.get('num_threads', 0)
            threads_item = QTableWidgetItem()
            threads_item.setData(Qt.ItemDataRole.EditRole, threads_val)
            self.setItem(row_num, 6, threads_item)

            self.setItem(row_num, 7, QTableWidgetItem(p_data.get('create_time_str', 'N/A')))

        self.setSortingEnabled(True)
        if sort_column != -1: # Restore sorting if it was set
            self.sortByColumn(sort_column, sort_order)

        # Restore the selection
        if 0 <= current_selected_row < self.rowCount():
            self.selectRow(current_selected_row)
        elif self.rowCount() > 0:
            self.selectRow(0) # Select the first row if the previous selection is invalid

    def get_selected_pid_and_name(self):
        selected_items = self.selectedItems()
        if not selected_items:
            return None, None

        current_row = self.currentRow()
        pid_item = self.item(current_row, 0)
        name_item = self.item(current_row, 1)

        if pid_item:
            try:
                pid = int(pid_item.text())
                name = name_item.text() if name_item else "Unknown name."
                return pid, name
            except ValueError:
                return None, None
        return None, None