"""
auto_CRP.py

This module coordinates the display of process list and detailed process info using npyscreen.

Copyright (C) 2024, Giang Trinh.
"""

import threading
import sys
from _2_display_module.CRP import CRP_window_module, One_proc_window_module
from error_code import *

CRP_window = [CRP_window_module.init_CRP_window,
              CRP_window_module.getkey_CRPwindow,
              CRP_window_module.exit_CRP_window]
PID_window = [One_proc_window_module.init_One_proc_window,
              One_proc_window_module.getkey_One_proc_window,
              One_proc_window_module.exit_One_proc_window]

CRP_thread1 = None
CRP_thread2 = None
CRP_thread3 = None
CRP_thread4 = None

PID_thread1 = None
PID_thread2 = None

def push_CRP_data_to_screen():
    CRP_window_module.push_to_screen()

def renew_list_precesses_data():
    CRP_window_module.renew_list_precesses_data()

def update_list_proc_display():
    CRP_window_module.update_list_proc_display()

def update_total_resource():
    CRP_window_module.update_total_resource()

def start_CRP_threads():
    global CRP_thread1, CRP_thread2, CRP_thread3, CRP_thread4
    CRP_thread1 = threading.Thread(target=push_CRP_data_to_screen)
    CRP_thread2 = threading.Thread(target=renew_list_precesses_data)
    CRP_thread3 = threading.Thread(target=update_list_proc_display)
    CRP_thread4 = threading.Thread(target=update_total_resource)
    CRP_thread1.start()
    CRP_thread2.start()
    CRP_thread3.start()
    CRP_thread4.start()

def destroy_CRP_threads():
    global CRP_thread1, CRP_thread2, CRP_thread3, CRP_thread4
    CRP_thread1.join()
    CRP_thread2.join()
    CRP_thread3.join()
    CRP_thread4.join()

def push_PID_data_to_screen():
    One_proc_window_module.push_to_screen()

def update_PID_properties():
    One_proc_window_module.update_PID_properties()

def start_PID_threads():
    global PID_thread1, PID_thread2
    PID_thread1 = threading.Thread(target=push_PID_data_to_screen)
    PID_thread2 = threading.Thread(target=update_PID_properties)
    PID_thread1.start()
    PID_thread2.start()

def destroy_PID_threads():
    global PID_thread1, PID_thread2
    PID_thread1.join()
    PID_thread2.join()

def CRP_auto_run():
    all_or_one = 0
    pid_chosen = 0
    ret = None
    while True:
        if all_or_one == 0:
            CRP_window[0]()
            start_CRP_threads()
            ret = CRP_window[1]()
            destroy_CRP_threads()
            CRP_window[2]()
            if ret >= 0:
                if debug == CommonErrorCode.DEBUG:
                    print(f"[OK - CRP_auto_run] - Opening PID [{ret}]", file=sys.stderr)
                all_or_one = 1
                pid_chosen = ret
            elif ret == -1:
                if debug == CommonErrorCode.DEBUG:
                    print("[OK - CRP_auto_run] - Open menu signal", file=sys.stderr)
                return 0
            elif ret == -2:
                print("[OK - CRP_auto_run] - Quit signal", file=sys.stderr)
                return -1
            elif ret < -2:
                print("[ERR - CRP_auto_run] - Unexpected event", file=sys.stderr)
                return -1
        elif all_or_one == 1:
            PID_window[0](pid_chosen)
            start_PID_threads()
            ret = PID_window[1]()
            destroy_PID_threads()
            PID_window[2]()
            if ret == -1:
                if debug == CommonErrorCode.DEBUG:
                    print(f"[OK - CRP_auto_run] - Opening CRP window [{ret}]", file=sys.stderr)
                all_or_one = 0
            elif ret == -2:
                print("[OK - CRP_auto_run] - Quit signal", file=sys.stderr)
                return -1
            elif ret < -2:
                print("[ERR - CRP_auto_run] - Unexpected event", file=sys.stderr)
                return -1