import npyscreen
from _4_system_data import CRP_control
from _1_auto_run.running_process import destroy_CRP_threads
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
        self.update_data()
        self.entry_widget.add_handlers({
            curses.KEY_ENTER: self.handle_selection,
            ord('\n'): self.handle_selection,
        })
        self.next_form = 'SECOND'  # Default next form

    def update_data(self):
        CRP_control.get_list_proc()
        sorted_procs = sorted(CRP_control.list_proc, key=lambda proc: proc['cpu_percent'], reverse=True)
        rows = []
        for proc in sorted_procs:
            row = f"{proc['pid']:<6} {proc['name'][:15]:<15} {proc['status']:<10} {proc['cpu_percent']:<8} {proc['memory_percent']:<8}"
            rows.append(row)

        self.entry_widget.values = rows
        self.entry_widget.display()
    
    def handle_selection(self, _):
        selected_string = self.entry_widget.values[self.entry_widget.cursor_line]
        try:
            destroy_CRP_threads()
            pid = int(selected_string.strip().split()[0])
            log.log_info("PID selected: {}".format(pid))
            # second_form = self.parent.parentApp.getForm('SECOND')
            self.parent.parentApp.getForm(self.next_form)
            second_form = self.parent.parentApp.getForm('SECOND') 

            second_form.process_box.set_pid(pid)
            # self.parent.parentApp.switchForm('SECOND')
            # destroy_CRP_threads()
        except (IndexError, ValueError):
            npyscreen.notify_wait("Không thể lấy PID từ dòng đã chọn.", title="Lỗi")
