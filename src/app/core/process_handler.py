import psutil
import datetime

def get_all_processes_info():
    processes_list = []
    attrs = ['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_info', 'num_threads', 'create_time']
    for proc in psutil.process_iter(attrs):
        try:
            p_info = proc.info
            p_info['create_time_str'] = datetime.datetime.fromtimestamp(p_info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
            p_info['memory_rss_mb'] = round(p_info['memory_info'].rss / (1024 * 1024), 2)
            processes_list.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes_list

def terminate_process_by_pid(pid):
    """
    Send a terminate signal to a process based on its PID.
    Return (True, "Success message") or (False, "Error message").
    """
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return True, f"The request to terminate the process (PID: {pid}) has been sent."
    except psutil.NoSuchProcess:
        return False, f"Process PID {pid} no longer exit."
    except psutil.AccessDenied:
        return False, f"Permission denied to terminate process with PID {pid}."
    except Exception as e:
        return False, f"Unknown error occurred while terminating process {pid}: {e}"