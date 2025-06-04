import threading 
import sys
import os
from log.log import Logger
import time
from _2_display_module.process.process_layout import ProcessBox
log = Logger(os.path.abspath("app.log"))

def running_processes(process_box):
    log.log_info("Starting Process Manager Application")
# Thread control
stop_event = threading.Event()  # Event to signal threads to stop
lock = threading.Lock()  # Lock for shared data access

# Thread functions
def push_CRP_data_to_screen(process_box):
    while 1:
        time.sleep(1)
        log.log_info("Updating process data")
        process_box.update_data()

def _push_resource_data(resource_box):
    while not stop_event.is_set():
        time.sleep(1)
        with lock:
            resource_box.update_data()
        log.log_info("ResourceBox updated")

def renew_list_processes_data():
    log.log_info("renew_list_processes_data")
    
def update_list_proc_display():
    log.log_info("update_list_proc_display")

def update_total_resource():
    log.log_info("update_list_proc_display")

# Start and stop CRP threads
def start_CRP_threads(process_box, resource_box):
    """Start all CRP threads."""
    global CRP_thread1, CRP_thread2, CRP_thread3, CRP_thread4
    stop_event.clear()  # Reset stop event
    thread1 = threading.Thread(target=push_CRP_data_to_screen, args=(process_box,) ,daemon=True)
    thread1.start()

    thread2 = threading.Thread(target=_push_resource_data, args=(resource_box,) ,daemon=True)
    # thread2.start()
    # CRP_thread1 = threading.Thread(target=push_CRP_data_to_screen, daemon=True)
    # CRP_thread2 = threading.Thread(target=renew_list_processes_data, daemon=True)
    # CRP_thread3 = threading.Thread(target=update_list_proc_display, daemon=True)
    # CRP_thread4 = threading.Thread(target=update_total_resource, daemon=True)
    # CRP_thread1.start()
    # CRP_thread2.start()
    # CRP_thread3.start()
    # CRP_thread4.start()

def destroy_CRP_threads():
    """Stop and join all CRP threads."""
    stop_event.set()  # Signal threads to stop
    for thread in [CRP_thread1, CRP_thread2, CRP_thread3, CRP_thread4]:
        if thread and thread.is_alive():
            thread.join(timeout=2.0)  # Wait up to 2 seconds
    log.log_info("Stopped CRP threads")

# Main function to run CRP window
def CRP_auto_run():
    try:
        while True:
            log.log_info("Initialized CRP window")

            start_CRP_threads()

            destroy_CRP_threads()

            log.log_info("Closed CRP window")

    except Exception as e:
        log.log_error(f"Error in CRP_auto_run")
        destroy_CRP_threads()  # Ensure threads are stopped on error
        return -1