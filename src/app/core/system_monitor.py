import psutil
import datetime

def get_cpu_usage():
    """
    Get total %CPU usage.
    """
    return psutil.cpu_percent(interval=None)

def get_memory_info():
    """
    Get info RAM. \\
    Return (total, used, percent).
    """
    mem = psutil.virtual_memory()
    return {
        "total_gb": mem.total / (1024**3),
        "used_gb": mem.used / (1024**3),
        "percent": mem.percent
    }

def get_swap_info():
    """
    Get info Swap. \\
    Return (total, used, percent).
    """
    swap = psutil.swap_memory() 
    if swap.total == 0:
        return None 
    return {
        "total_gb": swap.total / (1024**3),
        "used_gb": swap.used / (1024**3),
        "percent": swap.percent
    }