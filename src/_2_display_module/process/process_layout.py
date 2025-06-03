import npyscreen

class ProcessBox(npyscreen.BoxTitle):
    def __init__(self, screen, *args, **keywords):
        process_data = [
                ["1", "init", "Running"],
                ["2", "bash", "Running"],
                ["3", "python", "Sleeping"],
                ["4", "nginx", "Stopped"]
            ]
        header = f"{'PID':<6} {'NAME':<15} {'STATUS':<10}"
        rows = [f"{pid:<6} {name:<15} {status:<10}" for pid, name, status in process_data]

        keywords['values'] = [header] + rows
        keywords['name'] = "PROCESS LIST"
        keywords['editable'] = False
        keywords['scroll_exit'] = True
        super().__init__(screen, *args, **keywords)