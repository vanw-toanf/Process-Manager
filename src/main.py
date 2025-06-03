import sys
import os
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from _1_auto_run.main_form import MyApplication
from _1_auto_run.running_process import running_processes
from log.log import Logger
log = Logger("./app.log") 

def main():
    try:
        process_thread = threading.Thread(target=running_processes)
        process_thread.daemon = True  # Thread sẽ dừng khi chương trình chính dừng
        process_thread.start()
        # Hoặc chạy giao diện chính (tùy bạn muốn cái nào chạy trước)
        app = MyApplication()
        app.run()
        
    except KeyboardInterrupt:
        log.log_info("Application stopped by user")
    except Exception as e:
        log.log_error(f"Application error: {str(e)}")
        raise

if __name__ == '__main__':
    main()

    