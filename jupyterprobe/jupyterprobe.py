from jupyterprobe.process_utils import get_sessions_dataframe
from jupyterprobe.gpu_utils import merge_gpu_info
from jupyterprobe.memory_utils import get_memory_info_gpu_cpu
from jupyterprobe.register_utils import register_experiment, populate_team_in_results

try:
    from jupyterprobe.richUI import get_summary_panel, get_usage_table, console_print
except:
    from jupyterprobe.plainUI import get_summary_panel, get_usage_table, console_print

import os

class Probe:
    def __init__(self, domain, port, **kwargs):
        self.domain = domain
        self.port = port
        self.kwargs = kwargs
        self.pid = os.getpid()
        self.results = None

    def Monitor(self, top_n=5, show_team=False):
        self._connect_and_generate_results()
        self._display_results_UI(top_n, show_team)

    def MonitorTeam(self, top_n=5):
        self.Monitor(top_n=top_n, show_team=True)

    def Declare(self, owner, priority, project):
        self.notebook_path = self.get_path_by_PID(self.pid)
        self.register_dict = register_experiment(self.notebook_path, owner, priority, project)

    def _connect_and_generate_results(self):
        self.results = get_sessions_dataframe(self.domain, self.port, **self.kwargs)
        if self.results is not None:
            self.results = merge_gpu_info(self.results)
            self.results.sort_values('CPU Memory (%)', ascending=False, inplace=True)
        else:
            raise Exception('Failed to get Jupyter sessions')
        self.results = populate_team_in_results(self.results)

    def _display_results_UI(self, top_n, show_team=False):
        memory_info = get_memory_info_gpu_cpu()
        summary = get_summary_panel(self.results, self.pid, memory_info)
        usage = get_usage_table(self.results, top_n, is_team=False)
        if show_team:
            team =  get_usage_table(self.results, top_n, is_team=True)
            console = console_print([summary, usage, team])
        else:
            console = console_print([summary, usage])

    def get_all_session_details(self):
        if self.results is None:
            self._connect_and_generate_results()
        return self.results

    def get_results_by_PID(self, pid):
        if self.results is None:
            self._connect_and_generate_results()
        output = self.results[self.results['PID']==pid]
        if len(output)==0:
            print('PID {} not found. Please recheck'.format(pid))
            return None
        else:
            return output

    def get_results_by_name(self, name):
        if self.results is None:
            self._connect_and_generate_results()
        output = self.results[self.results['Name']==name]
        if len(output)==0:
            print('Name {} not found. Please recheck'.format(pid))
            return None
        else:
            return output

    def get_path_by_PID(self, pid):
        output = self.get_results_by_PID(pid)
        if output is None:
            return None
        else:
            return output['Path'].iloc[0]

    def get_path_by_name(self, name):
        output = self.get_results_by_name(name)
        if len(output)==1:
            return output['Path'].iloc[0]
        else:
            print('More than one notebooks with name {}'.format(name))
            return output[['Name', 'Path']].values

    def stop_notebook(self, pid):
        pass
