import pynvml
import pandas as pd
import re

def get_gpu_processes(pid_mapping={}):
    try:
        pynvml.nvmlInit()
    except Exception as e:
        print('WARN: GPU not supported on your system')
        return None
        # return pd.DataFrame({'PID': [], 'GPU Memory': [], 'GPU ID': []})
    pids = []
    memory_pcts = []
    # memory_usgs = [] TODO
    gpu_ids = []
    for gpu_id in range(pynvml.nvmlDeviceGetCount()):
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        for proc in pynvml.nvmlDeviceGetComputeRunningProcesses(handle):
            if len(pid_mapping.keys())==0 or proc.pid in pid_mapping.keys():
                memory_pcts.append(proc.usedGpuMemory/pynvml.nvmlDeviceGetMemoryInfo(handle).total*100)
                gpu_ids.append(gpu_id)
                if len(pid_mapping.keys())==0:
                    pids.append(proc.pid)
                else:
                    pids.append(pid_mapping[proc.pid])

    return pd.DataFrame({'PID': pids, 'GPU Memory': memory_pcts, 'GPU ID': gpu_ids})


def global_to_local_pid_mapping(local_pids):
    mapping = {}
    for local_pid in local_pids:
        path = '/proc/{}/task/{}/sched'.format(local_pid, local_pid)
        file = open(path, 'r')
        line = file.readline().rstrip()
        global_pid = re.findall(r'[(][\d]+,', line)[0][1:-1]
        mapping[int(global_pid)] = local_pid
    return mapping


def merge_gpu_info(df):
    mapping = global_to_local_pid_mapping(df['PID'].values)
    gpu_df = get_gpu_processes(pid_mapping=mapping)
    if gpu_df is None:
        return df
    out_df = pd.merge(df, gpu_df, on='PID', how='left')
    out_df['GPU Memory'] = out_df['GPU Memory'].fillna(0)
    out_df['GPU ID'] = out_df['GPU ID'].fillna('CPU')
    return out_df
