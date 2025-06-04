"""
File: CRP_control.py
Description: This Python script uses the 'psutil' library to monitor
and manage system processes.
It provides detailed information on running processes, system resource statistics,
and process management functionalities based on the process ID (PID).

Copyright (C) 2024  Giang Trinh, VuongNQ.

This file is part of the Process Manager project and is licensed
under the GNU General Public License v3 or later.
"""

'''****************************************************************************
* Definitions
****************************************************************************'''
import psutil
from datetime import datetime

'''****************************************************************************
* Variables, Const
****************************************************************************'''
# Note: For accurate data, functions should be called with an interval of 
# at least 1 second.

# [1. Variables for displaying the 'process list']
list_proc = None    # A list of dictionaries containing process details:
                    # Includes: "pid" (Process ID), "name" (Name), "cpu_percent" (CPU usage %),
                    # "memory_percent" (Memory usage %), "status" (Current status),
                    # "create_time" (Time the process has been running, formatted).

leng_proc = 0  # Count of processes in the list

total_core = psutil.cpu_count() # Total number of CPU cores.
                    # Note: "cpu_percent" returns the overall percentage
                    # across all cores for a process,
                    # so it must be divided by the number of cores to get per-core usage.

sort_order = 0  # Sorting order for the process list:
                # 0 = by PID, 1 = by Name, 2 = by %CPU, 3 = by %RAM,
                # 4 = by Status, 5 = by Runtime.

# [2. Variables for 'total system resource' statistics]
total_resource_info = None # Dictionary to store overall system statistics:
# Structure:
# {
#     "cpu_percent": CPU usage (%),
#     "total_ram": Total RAM (in MB),
#     "used_ram": Used RAM (in MB),
#     "current_time": Current time,
#     "total_pid": Total number of processes (PIDs),
#     "running": Count of running processes,
#     "sleeping": Count of sleeping processes,
#     "stopped": Count of stopped processes,
#     "zombie": Count of zombie processes,
# }

#  [3. Variables for handling a specific 'PID's properties]
PID_object = None # Reference to a Process object for actions like suspend, resume, terminate, or kill.
PID_properties = None  # Dictionary to store process properties as string values:
# Structure:
# {
#     "Name": Name of the process (str)
#     "Username": Username of the process owner (str)
#     "Status": Current status of the process (str)
#     "PID": Process ID (int)
#     "PPID": Parent Process ID (int)
#     "Command": Command line used to start the process (str)
#     "Executable": Path to the executable file (str)
#     "CWD": Current working directory of the process (str)
#     "MEM_VMS": Virtual memory size (in MB) (float)
#     "MEM_RSS": Resident Set Size, physical memory used (in MB) (float)
#     "MEM_Percent": Percentage of memory usage (str)
#     "CPU Num": The CPU core the process is running on (int)
#     "CPU Usage": Percentage of CPU usage (str)
#     "Runtime": Elapsed time since process creation (formatted as hh:mm:ss) (str)
#     "User Time": Total CPU time spent in user mode (float, seconds) (str)
#     "Sys Time": Total CPU time spent in system mode (float, seconds) (str)
#     "I/O Read Count": Number of read operations (int)
#     "I/O Write Count": Number of write operations (int)
#     "Open Files Count": Number of files currently opened by the process (int)
#     "Number of Threads": Number of threads in the process (int)
# }

'''****************************************************************************
* CODE
****************************************************************************'''
########## [Functions for process list management]
def format_elapsed_hhmmss(elapsed_time):
    """Format the elapsed time into hh:mm:ss."""
    seconds = int(elapsed_time.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02}:{seconds:02}"

def sort_by_order():
    '''Sort the process list based on the specified sorting criteria.'''
    global list_proc, sort_order
    if sort_order == 0:  # Sort by PID
        list_proc.sort(key=lambda p: p["pid"])
    elif sort_order == 1:  # Sort by process name
        list_proc.sort(key=lambda p: p["name"].lower())  # Case-insensitive sorting
    elif sort_order == 2:  # Sort by CPU usage (%)
        list_proc.sort(key=lambda p: float(p["cpu_percent"].rstrip('%')), reverse=True)
    elif sort_order == 3:  # Sort by RAM usage (%)
        list_proc.sort(key=lambda p: float(p["memory_percent"].rstrip('%')), reverse=True)
    elif sort_order == 4:  # Sort by process status
        list_proc.sort(key=lambda p: p["status"])
    elif sort_order == 5:  # Sort by runtime
        list_proc.sort(key=lambda p: p["create_time"])
    else:
        return  # No action for invalid sort_order

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

    # Reset the process list
    list_proc = []

    # Get the current time
    now = datetime.now()
    
    # Fetch process data
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status", "create_time"]):
        try:
            # Format each process's information
            proc_info = p.info
            proc_info["cpu_percent"] = proc_info["cpu_percent"] / total_core
            proc_info["cpu_percent"] = f"{proc_info['cpu_percent']:.1f}%"  # Format CPU usage
            proc_info["memory_percent"] = f"{proc_info['memory_percent']:.1f}%"  # Format RAM usage

            # Calculate elapsed runtime
            if "create_time" in proc_info and proc_info["create_time"] is not None:
                create_time = datetime.fromtimestamp(proc_info["create_time"])
                elapsed_time = now - create_time
                proc_info["create_time"] = format_elapsed_hhmmss(elapsed_time)

            # Append process information to the list
            list_proc.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Ignore inaccessible processes
            continue

    # Update process count
    leng_proc = len(list_proc)

    # Sort the process list based on the current order
    sort_by_order()

############ [Functions for system resource statistics]
def get_dict_total_resource():
    '''Collect and organize total system resource statistics.'''
    global total_resource_info

    # Initialize statistics
    total_resource_info = {
        "cpu_percent": 0,  # CPU usage (%)
        "total_ram": 0,  # Total RAM (MB)
        "used_ram": 0,  # Used RAM (MB)
        "current_time": 0,  # Current time
        "total_pid": 0,  # Total number of processes (PIDs)
        "running": 0,
        "sleeping": 0,
        "stopped": 0,
        "zombie": 0,
    }

    # Gather data
    total_resource_info["cpu_percent"] = psutil.cpu_percent(interval=None)
    total_resource_info["total_ram"] = psutil.virtual_memory().total // (1024 ** 2)
    total_resource_info["used_ram"] = psutil.virtual_memory().used // (1024 ** 2)
    total_resource_info["current_time"] = datetime.now().strftime("%H:%M")
    total_resource_info["total_pid"] = len(psutil.pids())

    for proc in psutil.process_iter(['status']):
        try:
            status = proc.info['status']
            if status == psutil.STATUS_RUNNING:
                total_resource_info["running"] += 1
            elif status == psutil.STATUS_SLEEPING:
                total_resource_info["sleeping"] += 1
            elif status == psutil.STATUS_STOPPED:
                total_resource_info["stopped"] += 1
            elif status == psutil.STATUS_ZOMBIE:
                total_resource_info["zombie"] += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def get_process_info(pid):
    """
    Retrieve and format properties for a given PID as a dictionary of strings.

    Args:
        pid (int): Process ID.

    Returns:
        int: Status code indicating success (0) or specific error (-1, -2, -3).
    """
    global PID_object
    global PID_properties
    global total_core
    try:
        PID_object = psutil.Process(pid)  # Tạo đối tượng Process
        info = PID_object.as_dict(attrs=[
            "name", "username", "status", "pid", "ppid", "cmdline",
            "exe", "cwd", "memory_info", "memory_percent",
            "cpu_num", "create_time",
            "num_threads", "io_counters", "open_files"
        ])
        # because of "cpu_percent" of Process object can't save to calculate next time
        # so we will using "process_iter" to get cpu_percent of this PID
        # the first value maybe 0% but it no problem.
        # read more at: https://psutil.readthedocs.io/en/latest/#processes
        info["cpu_percent"] = None
        for item in psutil.process_iter(["pid", "cpu_percent"]):
            if item.info["pid"] == pid:
                info["cpu_percent"] = item.info["cpu_percent"]/total_core
        if info["cpu_percent"] == None:
            return -4

        # Tính toán thời gian chạy của quá trình (Runtime)
        now = datetime.now()
        create_time = datetime.fromtimestamp(info["create_time"])
        runtime_seconds = now - create_time  # Thời gian chạy tính bằng giây
        runtime_formatted = format_elapsed_hhmmss(runtime_seconds)

        # Chuyển đổi VMS và RSS sang MB
        vms_mb = info["memory_info"].vms / (1024 * 1024) if info.get("memory_info") else "N/A"
        rss_mb = info["memory_info"].rss / (1024 * 1024) if info.get("memory_info") else "N/A"

        # Định dạng lại thông tin thành chuỗi
        PID_properties = {
            "Name": str(info.get("name", "N/A")),
            "Username": str(info.get("username", "N/A")),
            "Status": str(info.get("status", "N/A")),
            "PID": str(info.get("pid", "N/A")),
            "PPID": str(info.get("ppid", "N/A")),
            "Command": " ".join(info.get("cmdline", [])) if info.get("cmdline") else "N/A",
            "Executable": str(info.get("exe", "N/A")),
            "CWD": str(info.get("cwd", "N/A")),
            "MEM_VMS": f"{vms_mb:.2f}",#MB
            "MEM_RSS": f"{rss_mb:.2f}",#MB
            "MEM_Percent": f"{info.get('memory_percent', 'N/A'):.2f}",#(%)
            "CPU Num": str(info.get("cpu_num", "N/A")),
            "CPU Usage": f"{info.get('cpu_percent', 'N/A'):.2f}",#%
            "Runtime": runtime_formatted,#(hh:mm:ss)
            "User Time": f"{psutil.Process(pid).cpu_times().user:.3f}",#float second
            "Sys Time": f"{psutil.Process(pid).cpu_times().system:.3f}",#float second
            "I/O Read Count": str(info["io_counters"].read_count if info.get("io_counters") else "N/A"),
            "I/O Write Count": str(info["io_counters"].write_count if info.get("io_counters") else "N/A"),
            "Open Files Count": str(len(info.get("open_files")) if info.get("open_files") else "N/A"),
            "Num Threads": str(info.get("num_threads", "N/A")),
        }

    except psutil.NoSuchProcess:
        return -1
    except psutil.AccessDenied:
        return -2
    except psutil.ZombieProcess:
        return -3
    except Exception as e:
        return -4

    #ok 
    return 0