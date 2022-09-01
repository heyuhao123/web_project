from django.db import models

# Create your models here.


class UserInfo(models.Model):
    userID = models.CharField(max_length=32)
    tname = models.CharField(max_length=32)
    area = models.CharField(max_length=32)


"""class Tutors(models.Model):
    tutorID = models.CharField(max_length=32)
    tname = models.CharField(max_length=32)
    tarea = models.CharField(max_length=32)"""
