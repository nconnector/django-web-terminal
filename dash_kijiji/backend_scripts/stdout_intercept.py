"""
- run any command
- relay output to appropriate channel
- receive process object at the end

AppMonitor.cmd: initial command
AppMonitor.output_list: list of all stdout lines
AppMonitor.p: subprocess object
AppMonitor.p.pid: subprocess ID
"""

import subprocess
from ..models import Case


class Process:
    def __init__(self, cmd: list):
        self.cmd = cmd
        self.output_list = []
        print(f'running: {cmd}')
        self.p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        for path in self.monitor_process():
            self.message(path[:-1])  # strip \n at the end
            self.output_list.append(path[:-1])

    def monitor_process(self):
        for stdout_line in iter(self.p.stdout.readline, ""):
            yield stdout_line
        self.p.stdout.close()
        return_code = self.p.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, self.cmd)

    def message(self, msg):
        """relay the message"""
        case = Case.objects.get(id=2)
        case.log += f'\r\n{msg}'
        case.save()
