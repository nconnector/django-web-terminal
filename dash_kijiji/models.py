from django.db import models
# from djongo import models


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

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    log = models.TextField(default='')
    platform = models.CharField(
        max_length=200,
        choices=[
            ('kijiji', 'Kijiji.ca'),
            ('instagram', 'Instagram'),
                 ],
        default=None)
    # config is a hidden dict field, called only from backend
