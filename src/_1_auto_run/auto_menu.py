"""
auto_menu.py

This module coordinates the display of the menu page using npyscreen.

Copyright (C) 2024, Giang Trinh.
"""

import sys
import threading
from _2_display_module.menu import menu_window_module
from error_code import *

menu_window = [menu_window_module.init_menu_window,
               menu_window_module.get_choice_and_return,
               menu_window_module.exit_menu_window]

thread1 = None
thread2 = None

def update_menu_list():
    menu_window_module.update_menu_list()

def push_to_screen():
    menu_window_module.push_to_screen()

def start_threads():
    global thread1, thread2
    thread1 = threading.Thread(target=update_menu_list)
    thread2 = threading.Thread(target=push_to_screen)
    thread1.start()
    thread2.start()

def destroy_threads():
    global thread1, thread2
    thread1.join()
    thread2.join()

def menu_auto_run():
    max_num_choice = menu_window[0]()
    start_threads()
    ret = menu_window[1]()
    destroy_threads()
    menu_window[2]()
    if ret < -1 or ret >= max_num_choice:
        print("[ERR - menu_auto_run] - Unexpected event", file=sys.stderr)
    return ret