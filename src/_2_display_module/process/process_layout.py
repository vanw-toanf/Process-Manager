import npyscreen

class ProcessBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLine
    def __init__(self, screen, *args, **keywords):
        process_data = [
                ["1", "init", "Running"],
                ["2", "bash", "Running"],
                ["3", "python", "Sleeping"],
                ["4", "nginx", "Stopped"]
            ]
        rows = [f"{pid:<6} {name:<15} {status:<10}" for pid, name, status in process_data]

        keywords['values'] = rows
        keywords['name'] = "PROCESS LIST < PID - NAME - STATUS >"
        keywords['editable'] = True
        keywords['scroll_exit'] = True
        keywords['slow_scroll'] = True
        super().__init__(screen, *args, **keywords)