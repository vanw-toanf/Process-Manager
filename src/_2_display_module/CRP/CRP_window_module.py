"""
CRP_window_module.py

This module manages the process list interface using npyscreen.

Copyright (C) 2024, Giang Trinh.
"""

import npyscreen
import sys
import threading
from _3_display_component.CRP.CRP_win_component import CRPwin
from _4_system_data import CRP_control
from error_code import *

class CRPWindowModule:
    def __init__(self):
        self.w_CRP = None
        self.end_sig = CommonErrorCode.NOT_END_SIG
        self.mutex_R1 = threading.Lock()
        self.mutex_R2 = threading.Lock()
        self.mutex_R3 = threading.Lock()
        self.mutex_catch_screen = threading.Lock()
        self.condition_catch_screen = threading.Condition(self.mutex_catch_screen)
        self.catch_screen_sig = CommonErrorCode.NOT_STOP_SIG
        self.total_threads_stopped = 0
        self.cycle_renew_list_proc = 1
        self.cycle_update_list_proc = 0.3
        self.cycle_renew_and_update_list_total_resource = 1
        self.cycle_user_input = 0.2
        self.cycle_screen_refresh = 0.3
        self.sort_order = 0

    def renew_global_variable(self):
        self.end_sig = CommonErrorCode.NOT_END_SIG
        self.catch_screen_sig = CommonErrorCode.NOT_STOP_SIG
        self.total_threads_stopped = 0
        self.sort_order = 0

    def init_CRP_window(self):
        self.renew_global_variable()
        self.w_CRP = CRPwin(name="Process Manager")

    def getkey_CRPwindow(self):
        self.w_CRP.edit()
        if self.w_CRP.how_exited() == npyscreen.wgwidget.EXITED_ESCAPE:  # 'q'
            return -2
        elif self.w_CRP.how_exited() == -2:  # 'm'
            return -1
        elif self.w_CRP.how_exited() == -3:  # 'Enter'
            return CRP_control.list_proc[self.w_CRP.offset_list_proc + self.w_CRP.current_order_proc]["pid"]
        return -5

    def exit_CRP_window(self):
        if debug == CommonErrorCode.DEBUG:
            print("[OK - exit_CRP_window] closed the CRP window", file=sys.stderr)

    def push_to_screen(self):
        while self.end_sig == CommonErrorCode.NOT_END_SIG:
            with self.mutex_R1:
                self.w_CRP.display()
            threading.Event().wait(self.cycle_screen_refresh)

    def renew_list_precesses_data(self):
        while self.end_sig == CommonErrorCode.NOT_END_SIG:
            self.mutex_catch_screen.acquire()
            self.total_threads_stopped += 1
            while self.catch_screen_sig == CommonErrorCode.STOP_SIG:
                self.condition_catch_screen.wait()
            self.total_threads_stopped -= 1
            self.mutex_catch_screen.release()
            with self.mutex_R2:
                with self.mutex_R3:
                    self.w_CRP.renew_list_processes(self.sort_order)
            threading.Event().wait(self.cycle_renew_list_proc)

    def update_list_proc_display(self):
        while self.end_sig == CommonErrorCode.NOT_END_SIG:
            with self.mutex_R1:
                with self.mutex_R2:
                    with self.mutex_R3:
                        self.w_CRP.update_proc_content()
            threading.Event().wait(self.cycle_update_list_proc)

    def update_total_resource(self):
        while self.end_sig == CommonErrorCode.NOT_END_SIG:
            self.mutex_catch_screen.acquire()
            self.total_threads_stopped += 1
            while self.catch_screen_sig == CommonErrorCode.STOP_SIG:
                self.condition_catch_screen.wait()
            self.total_threads_stopped -= 1
            self.mutex_catch_screen.release()
            with self.mutex_R1:
                self.w_CRP.update_total_content()
            threading.Event().wait(self.cycle_renew_and_update_list_total_resource)