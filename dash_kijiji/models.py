from django.db import models

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

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(default='')  # todo: not required
    platform = models.CharField(
        max_length=200,
        choices=[
            ('kijiji', 'Kijiji.ca'),
            ('instagram', 'Instagram'),
                 ],
        default=None)
    #config = models.DICTFIELD() for actual app config to use
