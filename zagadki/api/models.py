# Create your models here.
from django.db import models

class Zagadki(models.Model):
    numer = models.IntegerField(unique=True)
    kod = models.CharField(max_length=255)

    def __str__(self):
        return f'Zagadka {self.numer}'