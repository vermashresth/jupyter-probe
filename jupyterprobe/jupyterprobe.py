from jupyterprobe.process_utils import get_sessions_dataframe
from jupyterprobe.gpu_utils import merge_gpu_info

try:
    from jupyterprobe.richUI import get_summary_panel, get_usage_table, console_print
except:
    from jupyterprobe.plainUI import get_summary_panel, get_usage_table, console_print


class Probe:
    def __init__(self, domain, port, **kwargs):
        self.results = get_sessions_dataframe(domain, port, **kwargs)
        if self.results is not None:
            self.results = merge_gpu_info(self.results)
            self.results.sort_values('CPU Memory (%)', ascending=False, inplace=True)
        else:
            raise Exception('Failed to get Jupyter sessions')

    def monitor(self, top_n=5):
        """
        Return a jupyter widget showing state of the Jupyter Environment .
        Args:
            host (str): host running jupyter server
            port (str): port running jupytrt server
        Returns:
            Jpyter widget monitor
        """
        summary = get_summary_panel(13.6, 73)
        usage = get_usage_table(self.results, top_n)
        console = console_print([summary, usage])

    def get_all_sessions(self):
        return self.results

    def get_path_by_pid(self, pid):
        output = self.results[self.results['PID']==pid]['Path']
        if len(output)==0:
            print('PID {} not found. Please recheck')
            return None
        else:
            return output.iloc[0]

    def get_path_by_name(self, name):
        output = self.results[self.results['Name']==name]['Path']
        if len(output)==0:
            print('Name {} not found. Please recheck')
            return None
        elif len(output)==1:
            return output.iloc[0]
        else:
            print('More than one notebooks with name {}'.format(name))
            return output.values

    def stop_notebook(self, pid):
        pass
