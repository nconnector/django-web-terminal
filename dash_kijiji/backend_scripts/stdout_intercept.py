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
import sys


def execute_and_stream(cmd):  # running python include -u flag: unbuffered
    def listen(cmd):
        print(f'running: {cmd}')
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        for stdout_line in iter(p.stdout.readline, ""):
            sys.stdout.flush()
            yield stdout_line
        p.stdout.close()
        return_code = p.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

    for path in listen(cmd):
        """relay the message"""
        msg = path[:-1]
        case = Case.objects.get(id=2)
        case.log += f'\r\n{msg}'
        case.save()