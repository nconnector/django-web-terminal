from django.db import models

# Create your models here.


class Client(models.Model):
    def __str__(self):
        return self.unm

    unm = models.CharField(max_length=32)
    pwd = models.CharField(max_length=16)


class Case(models.Model):
    def __str__(self):
        return self.sampleurl

    user = models.ForeignKey(Client, on_delete=models.CASCADE)  # todo: rename to client to account (check db renaming)
    sampleurl = models.CharField(max_length=200)  # todo: rename to url
    # todo: add ad_id, title and so on.....
    data = models.TextField(default='')
