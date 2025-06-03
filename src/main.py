import sys
import os
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from _1_auto_run.main_form import MyApplication
from _1_auto_run.running_process import start_CRP_threads
from log.log import Logger
log = Logger("./app.log") 

def main():
    try:
        process_thread = threading.Thread(target=start_CRP_threads)
        process_thread.daemon = True
        process_thread.start()
        app = MyApplication()
        app.run()
        
    except KeyboardInterrupt:
        log.log_info("Application stopped by user")
    except Exception as e:
        log.log_error(f"Application error: {str(e)}")
        raise

if __name__ == '__main__':
    main()

    