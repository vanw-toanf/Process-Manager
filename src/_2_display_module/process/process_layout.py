import npyscreen
from _4_system_data import CRP_control

class ProcessBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineAction

    def __init__(self, screen, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        self.name = "PROCESS LIST < PID - NAME - STATUS - CPU - MEMORY >"
        self.editable = True
        self.scroll_exit = True
        self.slow_scroll = True
        self.update_data()

    def update_data(self):
        CRP_control.get_list_proc()
        sorted_procs = sorted(CRP_control.list_proc, key=lambda proc: proc['cpu_percent'], reverse=True)
        rows = []
        for proc in sorted_procs:
            row = f"{proc['pid']:<6} {proc['name'][:15]:<15} {proc['status']:<10} {proc['cpu_percent']:<8} {proc['memory_percent']:<8}"
            rows.append(row)

        self.entry_widget.values = rows
        self.entry_widget.display()