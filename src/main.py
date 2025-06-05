import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import TaskManagerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = TaskManagerApp()
    main_window.show()
    sys.exit(app.exec())