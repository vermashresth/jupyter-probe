from jupyterprobe.process_utils import get_sessions_dataframe
from jupyterprobe.gpu_utils import merge_gpu_info
from jupyterprobe.memory_utils import get_memory_info_gpu_cpu
from jupyterprobe.register_utils import register_experiment

try:
    from jupyterprobe.richUI import get_summary_panel, get_usage_table, console_print
except:
    from jupyterprobe.plainUI import get_summary_panel, get_usage_table, console_print

import os

class Probe:
    def __init__(self, domain, port, **kwargs):
        self.results = get_sessions_dataframe(domain, port, **kwargs)
        if self.results is not None:
            self.results = merge_gpu_info(self.results)
            self.results.sort_values('CPU Memory (%)', ascending=False, inplace=True)
        else:
            raise Exception('Failed to get Jupyter sessions')
        self.pid = os.getpid()
        self.notebook_path = self.get_path_by_PID(self.pid)

    def monitor(self, top_n=5):
        """
        Return a jupyter widget showing state of the Jupyter Environment .
        Args:
            host (str): host running jupyter server
            port (str): port running jupytrt server
        Returns:
            Jupyter widget monitor
        """
        memory_info = get_memory_info_gpu_cpu()
        summary = get_summary_panel(memory_info)
        usage = get_usage_table(self.results, top_n)
        console = console_print([summary, usage])

    def declare(self, owner, priority, project):
        register_experiment(self.notebook_path, owner, priority, project)

    def get_all_session_details(self):
        return self.results

    def get_path_by_PID(self, pid):
        output = self.results[self.results['PID']==pid]['Path']
        if len(output)==0:
            print('PID {} not found. Please recheck'.format(pid))
            return None
        else:
            return output.iloc[0]

    def get_path_by_name(self, name):
        output = self.results[self.results['Name']==name]['Path']
        if len(output)==0:
            print('Name {} not found. Please recheck'.format(name))
            return None
        elif len(output)==1:
            return output.iloc[0]
        else:
            print('More than one notebooks with name {}'.format(name))
            return output.values

    def stop_notebook(self, pid):
        pass
