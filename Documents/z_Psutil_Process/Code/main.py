import psutil

class ProcessManager:
    def __init__(self):
        self.processes = [] #list process
        self.refresh_processes()
    
    def refresh_processes(self):
        #  refresh processes( update )
        self.processes =  [ proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_info', 'status'])
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status'])
        ]
    def get_process_by_pid(self, pid): #access process info by pid
        for process in self.processes:
            if process['pid'] == pid:
                return process
        return None
    
    def display_processes(self):
        print(f"{'PID':<10}{'Name':<20}{'CPU (%)':<10}{'Memory (RSS)':<15}{'Status':<10}")
        print("-" *70)
        for proc in self.processes:
            print(f"{proc['pid']:<10}{proc['name']:<20}{proc['cpu_percent']:<10.2f}"
                  f"{proc['memory_info'].rss / (1024 * 1024):<15.2f}{proc['status']:<10}")

if __name__ == "__main__":
    pm = ProcessManager()
    pm.display_processes()
    pm.refresh_processes()
    