from jupyterprobe.memory_utils import memory_usage_psutil
from jupyterprobe.register_utils import get_current_jpy_server_details, get_notebook_abs_path

import os
import subprocess
import pandas as pd
import psutil
import requests


def get_sessions_dataframe(domain, port, password=None):
    """Show table with info about running jupyter notebooks.

    Args:
        host: host of the jupyter server.
        port: port of the jupyter server.

    Returns:
        DataFrame with rows corresponding to running notebooks and following columns:
            * index: notebook kernel id.
            * path: path to notebook file.
            * pid: pid of the notebook process.
            * memory: notebook memory consumption in percentage.
    """
    server = get_current_jpy_server_details()
    if server['password'] and password is None:
        print('Your jupyter host is configured to authenticate from password but you have not provided it.')
        raise
    res = get_running_sessions(domain, port, password=password, token=server['token'])
    if 'message' in res:
        if res['message'] == 'Forbidden':
            print('ERROR: Failed to authenticate. Token or password wrong. Please recheck')
            return None
    res = process_sessions_info(res)
    sessions = [{'Kernel_ID': session['kernel']['id'],
                  'Relative Path': session['path'],
                  'Name': session['name'],
                  'State': session['kernel']['execution_state']} for session in res]
    df = pd.DataFrame(sessions)
    df = df.set_index('Kernel_ID')
    df.index.name = 'Kernel ID'

    df['Path'] = df.apply(lambda row: get_notebook_abs_path(server, row['Relative Path']), axis=1)
    df['PID'] = df.apply(lambda row: get_process_id(row.name), axis=1)
    df['CPU Memory (%)'] = df["PID"].apply(memory_usage_psutil)

    return df

def get_running_sessions(domain, port, password=None, token=None):
    s = requests.Session()
    base_url = 'http://{}:{}'.format(domain, port)
    if password and token :
        raise Exception('Only one of password and token can be given')
    elif password:
        try:
            s.get(base_url)
        except:
            print('Jupyter host and/or port are wrong. Please recheck.')
            raise
        data = {'password':password}
        data.update(s.cookies)
        s.post(base_url+"/login", data=data)
        headers = {}
    elif token:
        headers = {
            'Authorization': 'token {}'.format(token)
        }
    else:
        headers = {}
    try:
        res = s.get(base_url + "/api/sessions", headers=headers).json()
    except:
        print('Jupyter host and/or port are wrong. Please recheck.')
        raise
    return res


def process_sessions_info(res):
    for idx, session in enumerate(res):
        if session['name']=='':
             name = res[idx]['path'].split('/')[-1]
             res[idx]['name'] = name
             res[idx]['notebook']['name'] = name
    return res


def get_top_parent(pids):
    n_top_pids = 0
    top_pid = None
    for pid in pids:
        p = psutil.Process(pid)
        parent_pid = p.ppid()
        if parent_pid not in pids:
            n_top_pids+=1
            top_pid = pid
    assert n_top_pids==1, 'More than one pids are parent pid for a notebook'
    return top_pid


def get_process_id(name):
    """Return process ids found by (partial) name or regex.

    Source: https://stackoverflow.com/a/44712205/304209.
    >>> get_process_id('kthreadd')
    [2]
    >>> get_process_id('watchdog')
    [10, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 61]  # ymmv
    >>> get_process_id('non-existent process')
    []
    """
    # child = subprocess.Popen(['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
    # response = child.communicate()[0]
    # all_pids =  [int(pid) for pid in response.split()]
    child = subprocess.Popen('ps -ax -o pid,command | awk "!/awk/ && /{}/"'.format(name), stdout=subprocess.PIPE, shell=True)
    response = child.communicate()[0]
    all_pids = [int(i.strip().split(' ')[0]) for i in response.decode('utf-8').split('\n')[:-1]]
    top_pid = get_top_parent(all_pids)
    return top_pid
