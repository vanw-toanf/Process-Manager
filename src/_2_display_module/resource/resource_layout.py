import npyscreen

class ResourceBox(npyscreen.BoxTitle):
    def __init__(self, screen, *args, **keywords):
        resource_data = [
            ["CPU Usage", "35%"],
            ["Memory Usage", "2.5 GB / 8 GB"],
            ["Disk Usage", "40%"],
            ["Network", "Up: 200KB/s  Down: 500KB/s"]
        ]
        rows = [f"{key:<15}: {val}" for key, val in resource_data]
        keywords['values'] = rows
        keywords['name'] = "SYSTEM RESOURCE"
        keywords['editable'] = False
        keywords['scroll_exit'] = True
        super().__init__(screen, *args, **keywords)