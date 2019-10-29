import signal
from django.db import models
from pathlib import Path
from os import kill
# from djongo import models

from .backend_scripts.stdout_intercept import execute_and_stream


# Create your models here.
class Account(models.Model):
    def __str__(self):
        return self.unm
    unm = models.CharField(max_length=32)
    pwd = models.CharField(max_length=16)


class Case(models.Model):
    def __str__(self):
        """a __str__ call to instance returns the value below"""
        return f"{self.platform} : {self.title}"

    def log_last(self):
        return str(self.log).split('\r\n')[-1]

    def log_history(self, count):
        return str(self.log).split('\r\n')[count*-1:]

    def process_open(self):
        cwd = Path(self.cwd)  # example dash_kijiji/backend_scripts/
        script_path = cwd / self.script_name
        execute_and_stream(['python', '-u', str(script_path.absolute())], cwd)  # todo: python path

    def process_kill(self):
        if self.pid:
            kill(self.pid, signal.SIGTERM)
            print(f'Case {self.id} killed process: {self.pid}')
        else:
            print(f'ERROR attempting to kill the process: PID for this case is ')

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    log = models.TextField(default='')
    pid = models.IntegerField(null=True, default=None)
    platform = models.CharField(
        max_length=200,
        choices=[
            ('kijiji', 'Kijiji.ca'),
            ('instagram', 'Instagram'),
                 ],
        default=None)
    # config is a hidden dict field, called only from backend
