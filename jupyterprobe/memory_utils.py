import os
import psutil

def memory_usage_psutil(pid=None):
    """Get memory usage percentage by current process or by process specified by id, like in top.

    Source: https://stackoverflow.com/a/30014612/304209.

    Args:
        pid: pid of the process to analyze. If None, analyze the current process.

    Returns:
        memory usage of the process, in percentage like in top, values in [0, 100].
    """
    if pid is None:
        pid = os.getpid()
    process = psutil.Process(pid)
    return process.memory_percent()

def get_memory_info_gpu_cpu():
    res = {}
    cpu = psutil.virtual_memory()
    cpu_total = round(cpu[0]/2**30, 1)
    cpu_used = round(cpu[3]/2**30, 1)
    cpu_percent = cpu[2]
    res['CPU'] = {'total':cpu_total, 'used':cpu_used, 'percent':cpu_percent}
    try:
        import py3nvml.py3nvml as pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpu_total = round(gpu.total/2**30,1)
        gpu_used = round(gpu.used/2**30,1)
        gpu_percent = round(gpu_used/gpu_total, 3)*100
        res['GPU'] = {'total':gpu_total, 'used':gpu_used, 'percent':gpu_percent}
    except:
        pass
    return res
