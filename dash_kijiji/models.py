import json
import signal
from os import kill
from django.db import models
from pathlib import Path

from .backend_scripts.stdout_intercept import execute_and_stream


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

    def process_open(self):
        path = Path(Script.objects.get(id=self.script).script_path)
        cwd = path.parent
        # execute_and_stream will store case.pid
        execute_and_stream(['python', '-u', str(path.absolute())], cwd)  # todo: python path

    def process_kill(self):
        if self.pid:
            self.pid = None
            kill(self.pid, signal.SIGTERM)
            print(f'Case {self.id} killed process: {self.pid}')
        else:
            print(f'ERROR attempting to kill the process: PID for this case is ')

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
