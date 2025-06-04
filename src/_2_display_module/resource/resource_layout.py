import npyscreen
from _4_system_data import CRP_control      # nơi có get_dict_total_resource

class ResourceBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLine

    def __init__(self, screen, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        self.name = "SYSTEM RESOURCE"
        self.editable = False
        self.scroll_exit = True
        self.update_data()                  # lần đầu

    # gọi hàm thống kê & vẽ lại UI
    def update_data(self):
        CRP_control.get_dict_total_resource()
        info = CRP_control.total_resource_info      # dict đã chuẩn hoá sẵn

        rows = [
            f"CPU Usage      : {info['cpu_percent']:.1f} %",
            f"RAM            : {info['used_ram']} / {info['total_ram']}  MB",
            f"Processes      : {info['total_pid']}  (run: {info['running']}  sleep: {info['sleeping']})",
            f"Current Time   : {info['current_time']}",
        ]
        self.entry_widget.values = rows
        self.entry_widget.display()
