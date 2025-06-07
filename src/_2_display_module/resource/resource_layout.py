import npyscreen
from _3_system_data import CRP_control

class ResourceBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLine

    def __init__(self, screen, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        self.name = "SYSTEM RESOURCE"
        self.editable = False
        self.scroll_exit = True
        self.is_visible = True
        self.update_data()
    def update_data(self):
        if not getattr(self, "is_visible", True):
            return
        CRP_control.get_dict_total_resource()
        info = CRP_control.total_resource_info

        rows = [
            f"CPU Usage      : {info['cpu_percent']:.1f} %",
            f"RAM            : {info['used_ram']} / {info['total_ram']}  MB",
            f"Processes      : {info['total_pid']}  (run: {info['running']}  sleep: {info['sleeping']})",
            f"Current Time   : {info['current_time']}",
        ]
        self.entry_widget.values = rows
        if hasattr(self.entry_widget, 'display') and self.editing:
            self.entry_widget.display()
