# F101/models.py
from django.db import models


class Student(models.Model):
    """Model cực đơn giản"""
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name
