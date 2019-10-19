from django.db import models

# Create your models here.


class Client(models.Model):
    def __str__(self):
        return self.unm

    unm = models.CharField(max_length=32)
    pwd = models.CharField(max_length=16)


class Case(models.Model):
    def __str__(self):
        return self.data

    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    sampleurl = models.CharField(max_length=200)
    data = models.TextField(default='')


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)