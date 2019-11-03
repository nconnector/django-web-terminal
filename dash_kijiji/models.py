import sys
import subprocess
import json
import signal
import psutil
from os import kill
from django.db import models
from pathlib import Path

# from .backend_scripts.stdout_intercept import execute_and_stream


# Create your models here.
class Account(models.Model):
    def __str__(self):
        return self.unm
    unm = models.CharField(max_length=32)
    pwd = models.CharField(max_length=16)


class Script(models.Model):
    def __str__(self):
        return self.label

    label = models.CharField(max_length=32)
    script_path = models.TextField(default='dash_kijiji/backend_scripts/xxx.py')


class Case(models.Model):
    def __str__(self):
        """a __str__ call to instance returns the value below"""
        return f"{self.platform} : {self.title}"

    def log_last(self):
        return str(self.log).split('\r\n')[-1]

    def log_history(self, count):
        return str(self.log).split('\r\n')[count*-1:]

    def process_open(self):  # running python include -u flag: unbuffered
        path = Path(self.script.script_path)
        cwd = path.parent
        args = ''
        cmd = ['python', '-u', str(path.absolute()), args]  # todo: python path

        def listen():
            p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, shell=False, universal_newlines=True)
            self.pid = p.pid
            msg_open = f'case: {self.title} pid: {p.pid}'
            self.log += f'\r\n{msg_open}'
            print(f'{msg_open}  {cmd}')
            self.save()
            for stdout_line in iter(p.stdout.readline, ""):
                sys.stdout.flush()
                yield stdout_line
            p.stdout.close()
            return_code = p.wait()
            if return_code:
                yield False
                # raise subprocess.CalledProcessError(return_code, cmd)

        if not self.pid:
            for path in listen():
                # relay the message if it is str (not False)
                try:
                    msg = path[:-1]
                except TypeError:
                    break
                self.log += f'\r\n{msg}'
                self.save()
        else:
            print(f'ERROR: PID for {self.title} is not None. Kill PID {self.pid} and try again.')

    def process_kill(self):
        # kill process if it is alive
        if self.pid:
            msg_kill = f'Case {self.title} killing process: {self.pid}'
            print(msg_kill)
            try:
                kill(self.pid, signal.SIGTERM)
            except OSError:
                print('WARNING: there is no process with stored PID - it was closed from outside')
                print('Setting PID to None')
            self.pid = None
            self.log += f'\r\n{msg_kill}'
            self.save()
        else:
            print(f'ERROR: attempting to kill the process: PID for this case is {self.pid}')

    def process_status(self):
        # None - False, dead - False, alive - True
        if self.pid:
            try:
                psutil.Process(self.pid).status()
                return True
            except psutil.NoSuchProcess:
                return False
        else:
            return False

    # MODEL VARIABLES
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=160)
    email = models.EmailField()
    pwd = models.CharField(max_length=32)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)  # todo: add choice
    log = models.TextField(default='', blank=True)
    pid = models.IntegerField(null=True, blank=True, default=None)  # None while process is not running
    case_json_config = models.TextField(default='{}')  # todo: validate for double quotes '{"foo": "bar"}'


class Advert(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    advert_json_config = models.TextField(default='{}')  # todo: validate for double quotes '{"foo": "bar"}'
