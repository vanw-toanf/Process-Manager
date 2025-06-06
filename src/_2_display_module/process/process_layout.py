import npyscreen
from _4_system_data import CRP_control
from _1_auto_run.running_process import destroy_CRP_threads, pause_CRP_threads
import os
from log.log import Logger
log = Logger(os.path.abspath("app.log"))

import curses
class ProcessBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLine
    def __init__(self, screen, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        self.name = "PROCESS LIST < PID - NAME - STATUS - CPU - MEMORY >"
        self.editable = True
        self.scroll_exit = True
        self.slow_scroll = True
        self.is_visible = True
        self.update_data()
        self.entry_widget.add_handlers({
            ord('m'): self.handle_selection,
            ord('q'): self.terminate_process,
        })
        self.next_form = 'SECOND'  # Default next form

    def update_data(self):
        if not getattr(self, "is_visible", True):
            return
        CRP_control.get_list_proc()
        sorted_procs = sorted(CRP_control.list_proc, key=lambda proc: proc['cpu_percent'], reverse=True)
        rows = []
        for proc in sorted_procs:
            row = f"{proc['pid']:<6} {proc['name'][:15]:<15} {proc['status']:<10} {proc['cpu_percent']:<8} {proc['memory_percent']:<8}"
            rows.append(row)

        self.entry_widget.values = rows
        if hasattr(self.entry_widget, 'display') and self.editing:
            self.entry_widget.display()
    
    def handle_selection(self, _):
        try:
            selected_string = self.entry_widget.values[self.entry_widget.cursor_line]
            pid = int(selected_string.strip().split()[0])
            log.log_info(f"PID selected: {pid}")

            # Gọi callback nếu có
            if hasattr(self.parent, 'on_process_selected'):
                self.parent.on_process_selected(pid)
            # Ép thoát khỏi widget để Form có thể xử lý while_waiting
            self.entry_widget.editing = False
            if hasattr(self.parent, 'editing'):
                self.parent.editing = False
        except (IndexError, ValueError):
            npyscreen.notify_wait("Không thể lấy PID từ dòng đã chọn.", title="Lỗi")
            
    def terminate_process(self, _):
        selected_string = self.entry_widget.values[self.entry_widget.cursor_line]
        try:
            pid = int(selected_string.strip().split()[0])
            import psutil
            proc = psutil.Process(pid)
            proc.terminate()
            npyscreen.notify_confirm(f"Đã gửi tín hiệu terminate tới PID {pid}", title="Terminate")
            self.update_data()
        except Exception as e:
            npyscreen.notify_confirm(f"Lỗi khi terminate PID: {e}", title="Lỗi")

