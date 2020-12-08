from notebook import notebookapp
import os
import json

def get_current_jpy_server_details():
    servers = list(notebookapp.list_running_servers())
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

    json_file, json_file_path = get_json_register_file()
    dic = json.load(json_file)
    json_file.close()

    if id not in dic:
        dic[id] = {}

    notebook_name = notebook_id.split('/')[-1]
    if notebook_id in dic[id]:
        print('WARN: Found existing declaration for the current notebook')
        print('Owner: {}, Priority: {}, Project: {}'.format(
                                                            dic[id][notebook_id]['owner'],
                                                            dic[id][notebook_id]['priority'],
                                                            dic[id][notebook_id]['project']
        ))
        print('WARN: Declaration will be overwritten!')
    dic[id][notebook_id] = {'name': notebook_name, 'owner':owner, 'priority':priority, 'project':project}

    json_file = open(json_file_path, 'w+')
    json_file.write(json.dumps(dic))
    json_file.close()


def get_json_register_file():
    home_dir = os.path.expanduser('~')
    folder = '.jupyterprobe'
    file = 'experiment_register.json'
    register_file_path = os.path.join(home_dir, folder, file)

    if not os.path.exists(register_file_path):
        directory = os.path.dirname(register_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(register_file_path, 'w+')
        init_dict = {}
        f.write(json.dumps(init_dict))
        f.close()

    f = open(register_file_path, 'r')
    return f, register_file_path
