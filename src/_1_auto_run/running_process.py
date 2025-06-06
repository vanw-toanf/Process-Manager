import threading 
import sys
import os
from log.log import Logger
import time
from _4_system_data import CRP_control
log = Logger(os.path.abspath("app.log"))

# Thread control
stop_event = threading.Event()  # Event to signal threads to stop
is_paused = threading.Event()
is_paused.set()
lock = threading.Lock()  # Lock for shared data access

CRP_thread2= None
CRP_thread1 = None

# Thread functions
def push_process_running_data_to_screen(process_box):
    while not stop_event.is_set():
        is_paused.wait()
        time.sleep(2)
        log.log_info("Updating process data")
        process_box.update_data()

def push_resource_data(resource_box):
    while not stop_event.is_set():
        is_paused.wait()
        time.sleep(2)
        with lock:
            resource_box.update_data()
        log.log_info("ResourceBox updated")
        
# Start and stop CRP threads
def start_CRP_threads(process_box, resource_box):
    global CRP_thread1, CRP_thread2, stop_event, pause_event # <--- ĐẢM BẢO pause_event NẰM TRONG GLOBAL
    stop_event.clear()  # Reset stop event
    is_paused.set() # <--- Đảm bảo các luồng không bị tạm dừng khi khởi động

    # Chỉ khởi tạo và chạy luồng nếu nó chưa tồn tại hoặc đã dừng
    if CRP_thread1 is None or not CRP_thread1.is_alive():
        CRP_thread1 = threading.Thread(target=push_process_running_data_to_screen, args=(process_box,), daemon=True)
        CRP_thread1.start()
        log.log_info("CRP_thread1 started.")

    if CRP_thread2 is None or not CRP_thread2.is_alive():
        CRP_thread2 = threading.Thread(target=push_resource_data, args=(resource_box,), daemon=True)
        CRP_thread2.start()
        log.log_info("CRP_thread2 started.")

def pause_CRP_threads():
    is_paused.clear()  # ❌ Dừng lại
    log.log_info("CRP threads paused")

def resume_CRP_threads():
    is_paused.set()  # ✅ Cho phép chạy
    log.log_info("CRP threads resumed")
    
def destroy_CRP_threads():
    """Chỉ gọi khi thoát ứng dụng"""
    global stop_event, pause_event, CRP_thread1, CRP_thread2 # <--- ĐẢM BẢO stop_event VÀ pause_event NẰM TRONG GLOBAL
    try:
        stop_event.set()  # Signal threads to stop
        pause_event.clear() # Clear pause_event để các luồng có thể thoát vòng lặp wait()
        
        for thread in [CRP_thread1, CRP_thread2]:
            if thread and thread.is_alive():
                thread.join(timeout=1.0)
                if thread.is_alive():
                    log.log_warning(f"Thread {thread.name} không dừng")
    except Exception as e:
        log.log_error(f"Lỗi hủy threads: {str(e)}")

# Hàm CRP_auto_run này có thể gây xung đột nếu được gọi song song với việc quản lý luồng trong các form.
# Nếu bạn không gọi hàm này một cách có chủ đích, hãy đảm bảo rằng nó không được kích hoạt ở bất cứ đâu.
def CRP_auto_run(process_box, resource_box):
    log.log_info("CRP_auto_run called - this function might conflict with direct thread management in forms.")
    try:
        while True:
            time.sleep(1) 
    except Exception as e:
        log.log_error(f"Error in CRP_auto_run: {e}")
        destroy_CRP_threads()
        return -1