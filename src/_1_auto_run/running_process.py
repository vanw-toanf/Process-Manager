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

CRP_thread2= None
CRP_thread1 = None
# Thread functions
def push_process_running_data_to_screen(process_box):
    while not stop_event.is_set():
        time.sleep(2)
        log.log_info("Updating process data")
        process_box.update_data()
        
def push_resource_data(resource_box):
    while not stop_event.is_set():
        time.sleep(2)
        with lock:
            resource_box.update_data()
        log.log_info("ResourceBox updated")

def renew_list_processes_data():
    log.log_info("renew_list_processes_data")


# Start and stop CRP threads
def start_CRP_threads(process_box, resource_box):
    global CRP_thread1, CRP_thread2, stop_event
    stop_event.clear()  # Reset stop event
    CRP_thread1 = threading.Thread(target=push_process_running_data_to_screen, args=(process_box,), daemon=True)
    CRP_thread1.start()

    CRP_thread2 = threading.Thread(target=push_resource_data, args=(resource_box,), daemon=True)
    CRP_thread2.start()

def destroy_CRP_threads():
    """Stop and join all CRP threads."""
    stop_event.set()  # Signal threads to stop
    for thread in [CRP_thread1, CRP_thread2]:
        if thread and thread.is_alive():
            thread.join(timeout=2.0)  # Wait up to 2 seconds
    log.log_info("Stopped CRP threads")

def CRP_auto_run(process_box, resource_box):
    try:
        while True:
            log.log_info("Initialized CRP window")
            start_CRP_threads(process_box, resource_box)
            log.log_info("Closed CRP window")

    except Exception as e:
        log.log_error(f"Error in CRP_auto_run")
        destroy_CRP_threads()  # Ensure threads are stopped on error
        return -1