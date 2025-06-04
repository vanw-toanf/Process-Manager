"""
One_proc_window_module.py

This module manages the process detail interface using npyscreen.

Copyright (C) 2024, Giang Trinh.
"""

import npyscreen
import sys
import threading
from _3_display_component.CRP.One_proc_win_component import OneProcWin
from error_code import *

class OneProcWindowModule:
    def __init__(self):
        self.w_OneProc = None
        self.pid_input = None
        self.end_sig = CommonErrorCode.NOT_END_SIG
        self.lock_screen = threading.Lock()
        self.cycle_screen_refresh = 0.3
        self.cycle_properties_update = 1
        self.cycle_user_input = 0.2

    def renew_global_variable(self):
        self.end_sig = CommonErrorCode.NOT_END_SIG

    def init_One_proc_window(self, pid):
        self.pid_input = pid
        self.renew_global_variable()
        self.w_OneProc = OneProcWin(pid=pid, name="PID Properties")

    def getkey_One_proc_window(self):
        self.w_OneProc.edit()
        if self.w_OneProc.how_exited() == npyscreen.wgwidget.EXITED_ESCAPE:  # 'q'
            return -2
        elif self.w_OneProc.how_exited() == -2:  # 'l'
            return -1
        return -5

    def exit_One_proc_window(self):
        if debug == CommonErrorCode.DEBUG:
            print("[OK - exit_One_proc_window] closed the window", file=sys.stderr)

    def update_PID_properties(self):
        while self.end_sig == CommonErrorCode.NOT_END_SIG:
            with self.lock_screen:
                self.w_OneProc.get_and_update_PID_properties(self.pid_input)
            threading.Event().wait(self.cycle_properties_update)

    def push_to_screen(self):
        while self.end_sig == CommonErrorCode.NOT_END_SIG:
            with self.lock_screen:
                self.w_OneProc.display()
            threading.Event().wait(self.cycle_screen_refresh)