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
try:
    from ..models import Case
except ImportError as e:
    print(f'soft_warning: {__name__} {e}')


def execute_and_stream(cmd, cwd, case_id=1):  # running python include -u flag: unbuffered
    case = Case.objects.get(id=case_id)

    def listen(cmd, cwd):
        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, shell=False, universal_newlines=True)
        case.pid = p.pid
        print(f'case: {case.title} pid: {p.pid} running: {cmd}')
        for stdout_line in iter(p.stdout.readline, ""):
            sys.stdout.flush()
            yield stdout_line
        p.stdout.close()
        return_code = p.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

    if not case.pid:
        for path in listen(cmd, cwd):
            """relay the message"""
            msg = path[:-1]
            case.log += f'\r\n{msg}'
            case.save()
    else:
        print(f'ERROR: process for {case.title} is already present. Kill pid {case.pid} and try again.')
