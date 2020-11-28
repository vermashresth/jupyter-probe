import json
import os
import os.path
import posixpath
import subprocess
import urllib

import pandas as pd
import psutil

import requests

def get_running_sessions(domain, port, **kwargs):
    s = requests.Session()
    base_url = 'http://{}:{}'.format(domain, port)
    if 'password' in kwargs and 'token'in kwargs:
        raise 'only one of password and token can be supplied'
    elif 'password' in kwargs:
        s.get(base_url)
        data = {'password':kwargs['password']}
        data.update(s.cookies)
        s.post(base_url, "/login", data=data)
        headers = {}
    elif 'token' in kwargs:
        headers = {
            'Authorization': 'token {}'.format(kwargs['token'])
        }
    else:
        headers = {}
    res = s.get(base_url + "/api/sessions", headers=headers).json()
    return res

def process_sessions_info(res):
    for idx, session in enumerate(res):
        if session['name']=='':
             name = res[idx]['path'].split('/')[-1]
             res[idx]['name'] = name
             res[idx]['notebook']['name'] = name
    return res

def get_sessions_dataframe(host, port, **kwargs):
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
    res = get_running_sessions(host, port, **kwargs)
    res = process_sessions_info(res)
    sessions = [{'Kernel_ID': session['kernel']['id'],
                  'Path': session['path'],
                  'Name': session['name']} for session in res]
    df = pd.DataFrame(sessions)
    df = df.set_index('Kernel_ID')
    df.index.name = 'Kernel ID'
    df['PID'] = df.apply(lambda row: get_process_id(row.name), axis=1)
    df['CPU Memory'] = df["PID"].apply(memory_usage_psutil)
    return df.sort_values('CPU Memory', ascending=False)


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
    child = subprocess.Popen(['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    all_pids =  [int(pid) for pid in response.split()]
    top_pid = get_top_parent(all_pids)
    return top_pid


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
