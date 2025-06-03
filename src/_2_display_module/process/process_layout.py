import npyscreen
from _4_system_data import CRP_control
class ProcessBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLine
    def __init__(self, screen, *args, **keywords):
        CRP_control.get_list_proc()
        
        # Tạo các hàng để hiển thị từ list_proc
        rows = []
        for proc in CRP_control.list_proc:
            row = f"{proc['pid']:<6} {proc['name'][:15]:<15} {proc['status']:<10} {proc['cpu_percent']:<8} {proc['memory_percent']:<8}"
            rows.append(row)

        keywords['values'] = rows
        keywords['name'] = "PROCESS LIST < PID - NAME - STATUS >"
        keywords['editable'] = True
        keywords['scroll_exit'] = True
        keywords['slow_scroll'] = True
        super().__init__(screen, *args, **keywords)