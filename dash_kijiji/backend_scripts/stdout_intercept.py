"""
- run any command
- relay output to appropriate channel
- receive process object at the end

AppMonitor.cmd: initial command
AppMonitor.output_list: list of all stdout lines
AppMonitor.p: subprocess object
AppMonitor.p.pid: subprocess ID
"""

import sys
import subprocess
from ..models import Case


def execute_and_stream(cmd, cwd):  # running python include -u flag: unbuffered
    def listen(cmd, cwd):
        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, shell=False, universal_newlines=True)
        print(f'pid: {p.pid} running: {cmd}')
        for stdout_line in iter(p.stdout.readline, ""):
            sys.stdout.flush()
            yield stdout_line
        p.stdout.close()
        return_code = p.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

    for path in listen(cmd, cwd):
        """relay the message"""
        msg = path[:-1]
        case = Case.objects.get(id=1)  # todo: get ID from config
        case.log += f'\r\n{msg}'
        case.save()
