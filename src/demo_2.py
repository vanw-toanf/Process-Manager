import npyscreen
import threading
import time
from _3_system_data import CRP_control

class AutoUpdateProcessBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLine

    def __init__(self, screen, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        self.name = "PROCESS DETAILS (Auto-Update)"
        self.editable = False
        self.scroll_exit = True
        self.pid = None
        self.update_thread = None
        self.running = False
        self.lock = threading.Lock()

    def set_pid(self, pid):
        with self.lock:
            self.pid = pid
            if pid is not None:
                self._start_auto_update()

    def _start_auto_update(self, interval=1.0):
        if self.running:
            self._stop_auto_update()
        
        self.running = True
        self.update_thread = threading.Thread(
            target=self._update_loop,
            args=(interval,),
            daemon=True
        )
        self.update_thread.start()

    def _stop_auto_update(self):
        self.running = False
        if self.update_thread:
            self.update_thread.join(timeout=0.5)

    def _update_loop(self, interval):
        while self.running:
            with self.lock:
                current_pid = self.pid
                self._safe_update(current_pid)
            time.sleep(interval)

    def _safe_update(self, pid):
        if pid is None:
            return

        try:
            status = CRP_control.get_process_info(pid)
            if status < 0:
                self.entry_widget.values = [f"Error getting process info (code: {status})"]
            else:
                info = CRP_control.PID_properties
                rows = [
                    f"Name: {info['Name']}",
                    f"PID: {info['PID']} | PPID: {info['PPID']}",
                    f"Status: {info['Status']} | User: {info['Username']}",
                    f"CPU: {info['CPU Usage']}% (Core {info['CPU Num']})",
                    f"Memory: {info['MEM_VMS']}MB (RSS: {info['MEM_RSS']}MB, {info['MEM_Percent']}%)",
                    f"Runtime: {info['Runtime']}",
                    f"Threads: {info['Num Threads']} | I/O: R{info['I/O Read Count']}/W{info['I/O Write Count']}",
                    f"Last Update: {time.strftime('%H:%M:%S')}"
                ]
                self.entry_widget.values = rows
            
            # Thread-safe display update
            if hasattr(self, 'entry_widget'):
                self.entry_widget.display()
        except Exception as e:
            self.entry_widget.values = [f"Update error: {str(e)}"]
            self.entry_widget.display()

class ProcessMonitorForm(npyscreen.Form):
    def create(self):
        y, x = self.useable_space()
        
        # PID Input
        self.pid_input = self.add(
            npyscreen.TitleText,
            rely=2,
            relx=2,
            name="Enter PID:",
            use_two_lines=False
        )
        
        # Auto-updating Process Info
        self.process_box = self.add(
            AutoUpdateProcessBox,
            rely=5,
            relx=2,
            max_height=12,
            max_width=x-4
        )
        
        # Control Buttons
        self.add_btn = self.add(
            npyscreen.ButtonPress,
            rely=19,
            relx=2,
            name="Set PID",
            when_pressed_function=self.on_set_pid
        )
        
        self.exit_btn = self.add(
            npyscreen.ButtonPress,
            rely=19,
            relx=20,
            name="Exit",
            when_pressed_function=self.on_exit
        )

    def on_set_pid(self):
        try:
            pid = int(self.pid_input.value)
            self.process_box.set_pid(pid)
        except ValueError:
            self.process_box.entry_widget.values = ["Invalid PID!"]
            self.process_box.entry_widget.display()

    def on_exit(self):
        self.process_box._stop_auto_update()
        self.parentApp.switchForm(None)

class AutoUpdateProcessApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", ProcessMonitorForm, name="Auto-Update Process Monitor")

if __name__ == "__main__":
    app = AutoUpdateProcessApp()
    app.run()