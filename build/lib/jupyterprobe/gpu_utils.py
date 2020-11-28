import pynvml

def get_gpu_processes(pid_mapping):
    pynvml.nvmlInit()
    pids = []
    memory_pcts = []
    # memory_usgs = []
    gpu_ids = []
    for gpu_id in range(pynvml.nvmlDeviceGetCount()):
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        for proc in pynvml.nvmlDeviceGetComputeRunningProcesses(handle):
            if proc.pid in pid_mapping.keys():
                pids.append(pid_mapping[proc.pid])
                memory_pcts.append(float(proc.usedGpuMemory)/2**20)
                gpu_ids.append(gpu_id)
    return pd.DataFrame({'PID': pids, 'GPU Memory': memory_pcts, 'GPU ID': gpu_ids})

def global_to_local_pid_mapping(local_pids):
    mapping = {}
    for local_pid in local_pids:
        path = '/proc/{}/task/{}/sched'.format(pid)
        file = open(path, 'r')
        line = file.readline().rstrip()
        global_pid = re.findall(r'[(][\d]+,', line)[0][1:-1]
        mapping[int(global_pid)] = local_pid
    return mapping
