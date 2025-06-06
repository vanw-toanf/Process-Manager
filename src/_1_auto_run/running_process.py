import threading 
import sys
import os
from log.log import Logger
import time
import npyscreen

log = Logger(os.path.abspath("app.log"))

class ThreadManager:
    def __init__(self):
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.threads = []
        
    def start_threads(self, process_box, resource_box):
        """Khởi chạy các thread với cơ chế restart an toàn"""
        self.stop_event.clear()
        
        # Tạo thread mới nếu thread cũ đã dừng hoặc chưa tồn tại
        if not hasattr(self, 'CRP_thread1') or not self.CRP_thread1.is_alive():
            self.CRP_thread1 = threading.Thread(
                target=self.push_process_running_data_to_screen,
                args=(process_box,),
                daemon=True
            )
            self.CRP_thread1.start()
            self.threads.append(self.CRP_thread1)

        if not hasattr(self, 'CRP_thread2') or not self.CRP_thread2.is_alive():
            self.CRP_thread2 = threading.Thread(
                target=self.push_resource_data,
                args=(resource_box,),
                daemon=True
            )
            self.CRP_thread2.start()
            self.threads.append(self.CRP_thread2)

    def push_process_running_data_to_screen(self, process_box):
        """Cập nhật dữ liệu tiến trình an toàn"""
        while not self.stop_event.is_set():
            try:
                time.sleep(2)
                if hasattr(process_box, 'update_data'):
                    # Sử dụng npyscreen thread-safe để cập nhật UI
                    npyscreen.async_safe_call(process_box.update_data)
                    log.log_debug("Process data updated")
            except Exception as e:
                log.log_error(f"Error in process update: {str(e)}")

    def push_resource_data(self, resource_box):
        """Cập nhật dữ liệu tài nguyên an toàn"""
        while not self.stop_event.is_set():
            try:
                time.sleep(2)
                if hasattr(resource_box, 'update_data'):
                    with self.lock:
                        npyscreen.async_safe_call(resource_box.update_data)
                    log.log_debug("Resource data updated")
            except Exception as e:
                log.log_error(f"Error in resource update: {str(e)}")

    def stop_threads(self, wait_timeout=1.0):
        """Dừng các thread một cách an toàn"""
        self.stop_event.set()
        
        for thread in self.threads:
            if thread and thread.is_alive():
                thread.join(wait_timeout)
                
        self.threads = []
        log.log_info("All threads stopped")

# Sử dụng singleton pattern để quản lý thread
thread_manager = ThreadManager()

def start_CRP_threads(process_box, resource_box):
    thread_manager.start_threads(process_box, resource_box)

def destroy_CRP_threads():
    thread_manager.stop_threads()

def CRP_auto_run(process_box, resource_box):
    try:
        start_CRP_threads(process_box, resource_box)
        log.log_info("CRP threads started successfully")
    except Exception as e:
        log.log_error(f"CRP initialization failed: {str(e)}")
        destroy_CRP_threads()