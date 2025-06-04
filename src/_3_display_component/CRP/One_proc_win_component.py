"""
One_proc_win_component.py

This module defines the OneProcWin class for displaying process details using npyscreen.

Copyright (C) 2024  Giang Trinh.
"""

import npyscreen
from _3_display_component.container_class.container import Container
from _4_system_data import CRP_control

class OneProcWin(npyscreen.Form, Container):
    def __init__(self, pid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Container.__init__(self)
        self.pid = pid
        self.enable_sigterm = False

    def create(self):
        self.name = "PID Properties"

        # Thông tin cơ bản
        self.w_proc = self.add(
            npyscreen.BoxTitle,
            name="Process Info",
            values=[],
            max_height=15,
            editable=False
        )

        # Hướng dẫn và nút điều khiển
        self.w_guide = self.add(
            npyscreen.BoxTitle,
            name="How to use",
            values=["s-Suspend | r-Resume | t-Terminate | k-Kill | q-Quit | l-List"],
            max_height=3,
            editable=False
        )

        self.add(npyscreen.ButtonPress, name="Enable SIGTERM (u)", when_pressed_function=self.enable_sigterm_action)
        self.add(npyscreen.ButtonPress, name="Suspend (s)", when_pressed_function=lambda: self.send_sig(0))
        self.add(npyscreen.ButtonPress, name="Resume (r)", when_pressed_function=lambda: self.send_sig(1))
        self.add(npyscreen.ButtonPress, name="Terminate (t)", when_pressed_function=lambda: self.send_sig(2))
        self.add(npyscreen.ButtonPress, name="Kill (k)", when_pressed_function=lambda: self.send_sig(3))

        # Cập nhật dữ liệu ban đầu
        self.get_and_update_PID_properties(self.pid)

    def enable_sigterm_action(self):
        self.enable_sigterm = True
        self.w_guide.footer = "[SIGTERM Enabled]"
        self.w_guide.display()

    def get_and_update_PID_properties(self, pid):
        ret = CRP_control.get_process_info(pid)
        if ret != 0:
            self.w_proc.values = [f"Error: {['PID Not Found', 'Access Denied', 'Zombie Process', 'Unexpected Error'][abs(ret)-1]}"]
        else:
            self.w_proc.values = [
                f"Name: {CRP_control.PID_properties['Name']}",
                f"PID: {CRP_control.PID_properties['PID']} | PPID: {CRP_control.PID_properties['PPID']}",
                f"Status: {CRP_control.PID_properties['Status']} | Username: {CRP_control.PID_properties['Username']}",
                f"Command: {CRP_control.PID_properties['Command'][:50]}",
                f"Executable: {CRP_control.PID_properties['Executable'][:50]}",
                f"CWD: {CRP_control.PID_properties['CWD'][:50]}",
                f"Memory: VMS {CRP_control.PID_properties['MEM_VMS']}MB | RSS {CRP_control.PID_properties['MEM_RSS']}MB | {CRP_control.PID_properties['MEM_Percent']}%",
                f"CPU: Num {CRP_control.PID_properties['CPU Num']} | Usage {CRP_control.PID_properties['CPU Usage']}% | Threads {CRP_control.PID_properties['Num Threads']}",
                f"Runtime: {CRP_control.PID_properties['Runtime']} | User {CRP_control.PID_properties['User Time']}s | Sys {CRP_control.PID_properties['Sys Time']}s",
                f"I/O: Read {CRP_control.PID_properties['I/O Read Count']} | Write {CRP_control.PID_properties['I/O Write Count']} | Files {CRP_control.PID_properties['Open Files Count']}"
            ]
        self.w_proc.display()

    def send_sig(self, your_order):
        if not self.enable_sigterm:
            return
        try:
            if your_order == 0:
                CRP_control.PID_object.suspend()
            elif your_order == 1:
                CRP_control.PID_object.resume()
            elif your_order == 2:
                CRP_control.PID_object.terminate()
            elif your_order == 3:
                CRP_control.PID_object.kill()
        except Exception:
            pass
        self.get_and_update_PID_properties(self.pid)