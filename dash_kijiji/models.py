import sys
import subprocess
import json
import signal
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

    def test(self):
        print("TESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTING")  # todo: remove
        return ''

    def log_history(self, count):
        return str(self.log).split('\r\n')[count*-1:]

    def get_config(self):
        return json.loads(self.json_config.replace('\r\n', ''))

    def process_open(self):  # running python include -u flag: unbuffered
        path = Path(self.script.script_path)
        cwd = path.parent
        cmd = ['python', '-u', str(path.absolute())]  # todo: python path

        def listen():
            p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, shell=False, universal_newlines=True)
            self.pid = p.pid
            print(f'case: {self.title} pid: {p.pid} running: {cmd}')
            for stdout_line in iter(p.stdout.readline, ""):
                sys.stdout.flush()
                yield stdout_line
            p.stdout.close()
            return_code = p.wait()
            if return_code:
                raise subprocess.CalledProcessError(return_code, cmd)

        if not self.pid:
            for path in listen():
                """relay the message"""
                msg = path[:-1]
                self.log += f'\r\n{msg}'
                self.save()
        else:
            print(f'ERROR: PID for {self.title} is not None. Kill PID {self.pid} and try again.')

    def process_kill(self):
        if self.pid:
            print(f'Case {self.id} killing process: {self.pid}')
            try:
                kill(self.pid, signal.SIGTERM)
            except OSError:
                print(f'Looks like the process has been killed already. {self.pid}')
            finally:
                self.pid = None
                self.save()
        else:
            print(f'ERROR attempting to kill the process: PID for this case is {self.pid}')

    # MODEL VARIABLES
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    log = models.TextField(default='', blank=True)
    pid = models.IntegerField(null=True, blank=True, default=None)  # None while process is not running
    json_config = models.TextField(default='{}')  # todo: validate for double quotes '{"foo": "bar"}'
    platform = models.CharField(  # todo: remove as unnecessary or keep as label?
        max_length=200,
        choices=[
            ('kijiji', 'Kijiji.ca'),
            ('instagram', 'Instagram'),
                 ],
        default=None)
