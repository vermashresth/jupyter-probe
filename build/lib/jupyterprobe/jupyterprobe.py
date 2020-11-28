from jupyterprobe.process_utils import get_sessions_dataframe
try:
    from jupyterprobe.richUI import get_summary_panel, get_usage_table, console_print
except:
    from jupyterprobe.plainUI import get_summary_panel, get_usage_table, console_print

class Probe:
    def __init__(self, domain, port, **kwargs):
        self.results = get_sessions_dataframe(domain, port, **kwargs)

    def monitor(self):
        """
        Return a jupyter widget showing state of the Jupyter Environment .
        Args:
            host (str): host running jupyter server
            port (str): port running jupytrt server
        Returns:
            Jpyter widget monitor
        """
        summary = get_summary_panel(13.6, 73)
        usage = get_usage_table(self.results, 5)
        console = console_print([summary, usage])

    def get_all_sessions(self):
        return self.results

    def get_path_by_pid(self, pid):
        return self.results[self.results['PID']==pid]['path'][0]

    def get_path_by_name(self, name):
        output = self.results[self.results['Name']==name]['path']
        if len(output)==1:
            return output[0]
        else:
            print('More than one notebooks with name {}'.format(name))
            return output.values

    def stop_notebook(self, pid):
        pass
