from django.db import models

# Create your models here.


class Client(models.Model):
    unm = models.CharField(max_length=32)
    pwd = models.CharField(max_length=16)


class Case(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    sampleurl = models.CharField(max_length=200)
    data = models.TextField(default='')

