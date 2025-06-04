"""
menu_window_module.py

This module manages the menu interface using npyscreen.

Copyright (C) 2024  Giang Trinh.
"""

import npyscreen
import sys
import threading
from _3_display_component.menu.menu_win_component import Main_win
from error_code import *

class MenuWindowModule:
    def __init__(self):
        self.w_menu = None
        self.end_sig = CommonErrorCode.NOT_END_SIG
        self.lock_screen = threading.Lock()
        self.cycle_menu_update = 0.2
        self.cycle_screen_refresh = 0.3

    def renew_global_variable(self):
        self.end_sig = CommonErrorCode.NOT_END_SIG

    def init_menu_window(self):
        self.renew_global_variable()
        self.w_menu = Main_win(name="Task Manager")
        return self.w_menu.max_num_choice

    def get_choice_and_return(self):
        # Hiển thị form và chờ người dùng chọn
        self.w_menu.edit()
        choice = self.w_menu.get_order()

        # Xử lý lựa chọn
        if self.w_menu.how_exited() == npyscreen.wgwidget.EXITED_ESCAPE:  # Người dùng nhấn 'q' hoặc ESC
            print("[OK - get_choice_and_return] - Quit signal", file=sys.stderr)
            return -1
        return choice

    def exit_menu_window(self):
        if debug == CommonErrorCode.DEBUG:
            print("[OK - exit_menu_window] closed the menu window", file=sys.stderr)

    # Thread để cập nhật danh sách menu (nếu cần)
    def update_menu_list(self):
        while self.end_sig == CommonErrorCode.NOT_END_SIG:
            with self.lock_screen:
                self.w_menu.display()
            threading.Event().wait(self.cycle_menu_update)

    def push_to_screen(self):
        while self.end_sig == CommonErrorCode.NOT_END_SIG:
            with self.lock_screen:
                self.w_menu.display()
            threading.Event().wait(self.cycle_screen_refresh)