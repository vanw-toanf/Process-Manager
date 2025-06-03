import npyscreen

class MenuBox(npyscreen.BoxTitle):
    def __init__(self, screen, *args, **keywords):
        Menu_data = [
                ["ENTER", "More infor"],
                ["C", "Catch"],
                ["Q", "Quit"],
                ["M", "Menu"]
            ]
        Menu_rows = [f"{key:<15}: {val}" for key, val in Menu_data]
        keywords['values'] = Menu_rows
        keywords['name'] = "SYSTEM RESOURCE"
        keywords['editable'] = False
        keywords['scroll_exit'] = True
        super().__init__(screen, *args, **keywords)