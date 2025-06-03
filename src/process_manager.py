import psutil
from datetime import datetime
import logging

# Thiết lập logging
logging.basicConfig(level=logging.DEBUG, filename="process_manager.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")


# ... (các khai báo biến toàn cục khác giữ nguyên)

def get_list_proc():
    '''
    [Retrieve process information]
    Observations indicate that using psutil.process_iter.cache_clear() as suggested at
    https://psutil.readthedocs.io/en/latest/ results in 0% CPU usage being reported.
    This is because CPU usage calculations depend on previously retrieved data.
    Require: this function should run after at least 100ms (not < 100ms)
    '''
    global list_proc
    global leng_proc

    logging.debug("Starting get_list_proc")
    list_proc = []

    # Get the current time
    now = datetime.now()

    try:
        # Fetch process data
        process_count = 0
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status", "create_time"]):
            try:
                # Format each process's information
                proc_info = p.info
                proc_info["cpu_percent"] = proc_info["cpu_percent"] / total_core
                proc_info["cpu_percent"] = f"{proc_info['cpu_percent']:.1f}%"
                proc_info["memory_percent"] = f"{proc_info['memory_percent']:.1f}%"

                # Calculate elapsed runtime
                if "create_time" in proc_info and proc_info["create_time"] is not None:
                    create_time = datetime.fromtimestamp(proc_info["create_time"])
                    elapsed_time = now - create_time
                    proc_info["create_time"] = format_elapsed_hhmmss(elapsed_time)

                list_proc.append(proc_info)
                process_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                logging.warning(f"Skipped process due to: {str(e)}")
                continue
        logging.debug(f"Collected {process_count} processes")
    except Exception as e:
        logging.error(f"Error in get_list_proc: {str(e)}")
        list_proc = []
        return

    # Update process count
    leng_proc = len(list_proc)
    logging.debug(f"Total processes after sorting: {leng_proc}")

    # Sort the process list based on the current order
    sort_by_order()