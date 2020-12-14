from notebook import notebookapp
import os
import json
import pandas as pd
from filelock import Timeout, FileLock

def get_current_jpy_server_details():
    try:
        servers = list(notebookapp.list_running_servers())
    except:
        raise Exception('Could not connect to jupyter server from your kernel. Make sure you have Jupyter library installed for your current python kernel. \
        Try `pip uninstall -y jupyter jupyterlab && pip install jupyter jupyterlab` for your current python kernel')

    jpy_parent_pid = os.environ['JPY_PARENT_PID']
    for server in servers:
        if server['pid'] == int(jpy_parent_pid):
            break
    return server

def get_unique_jpy_identfier(server):
    return server['notebook_dir'] + ':' + str(server['port'])

def get_notebook_abs_path(server, notebook_rel_path):
    return os.path.join(server['notebook_dir'], notebook_rel_path)

def register_experiment(notebook_id, owner, priority, project):
    server = get_current_jpy_server_details()
    id = get_unique_jpy_identfier(server)

    dic, json_file, json_file_path = read_register_file()

    notebook_name = notebook_id.split('/')[-1]
    if notebook_id in dic:
        print('WARN: Found existing declaration for the current notebook')
        print('Owner: {}, Priority: {}, Project: {}'.format(
                                                            dic[notebook_id]['owner'],
                                                            dic[notebook_id]['priority'],
                                                            dic[notebook_id]['project']
        ))
        print('WARN: Declaration will be overwritten!')
    if not (isinstance(priority, int) or isinstance(priority, float)):
        raise ValueError('Priority argument must be an integer or float')

    dic[notebook_id] = {'name': notebook_name, 'owner':owner, 'priority':priority, 'project':project}

    lock = FileLock(json_file_path+'.lock')
    try:
        with lock.acquire(timeout=10):
            json_file = open(json_file_path, 'w+')
            json_file.write(json.dumps(dic))
    except Timeout:
        print("Another user is simultaneously declaring experiment. Please try declaring again.")

    return dic

def read_register_file():
    json_file, json_file_path = get_json_register_file()
    dic = json.load(json_file)
    json_file.close()
    return dic, json_file, json_file_path

def get_json_register_file():
    home_dir = os.path.expanduser('~')
    folder = '.jupyterprobe'
    file = 'experiment_register.json'
    register_file_path = os.path.join(home_dir, folder, file)

    if not os.path.exists(register_file_path):
        directory = os.path.dirname(register_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        lock = FileLock(register_file_path+'.lock')
        try:
            with lock.acquire(timeout=10):
                f = open(register_file_path, 'w+')
                init_dict = {}
                f.write(json.dumps(init_dict))
        except Timeout:
            print("Another user is simultaneously creating initial experiment register. Please try running your operation again.")


    f = open(register_file_path, 'r')
    return f, register_file_path

def populate_team_in_results(results):
    experiment_dict, _, _ = read_register_file()
    server = get_current_jpy_server_details()
    id = get_unique_jpy_identfier(server)
    values = []
    for experiment in experiment_dict:
        experiment_details = experiment_dict[experiment]

        name = experiment_details['name']
        owner = experiment_details['owner']
        priority =  experiment_details['priority']
        project =  experiment_details['project']

        values.append([experiment, name, owner, priority, project])

    df_team = pd.DataFrame(values, columns = ['Path', 'Name', 'Owner', 'Priority', 'Project'])
    out_df = pd.merge(results, df_team , how='left')
    out_df = out_df.fillna('-')
    return out_df
