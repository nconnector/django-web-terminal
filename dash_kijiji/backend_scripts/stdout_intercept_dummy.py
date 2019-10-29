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
sys.path.append("..")


def execute_and_stream(cmd, cwd):  # running python include -u flag: unbuffered
    def listen(cmd, cwd):
        print(f'running: {cmd} at cwd {cwd}')
        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
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
        print(msg)


script_name = 'telegram'
path = f'dash_kijiji\\backend_scripts\\{script_name}.py'  # todo: to config
cwd = '.\\'+'\\\\'.join(path.split('\\')[:-1])  # todo: to config
execute_and_stream(['python', '-u', path], cwd)
