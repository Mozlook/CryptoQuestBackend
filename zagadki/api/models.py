from django.contrib.auth.models import AbstractUser
from django.db import models

class Zagadki(models.Model):
    numer = models.IntegerField(unique=True)
    kod = models.CharField(max_length=255)

    def __str__(self):
        return f'Zagadka {self.numer}'

class Bledy(models.Model):
    numer = models.CharField(max_length=25)
    opis = models.CharField(max_length=255)

    def __str__(self):
        return f"Zagadka {self.numer}"

class CustomUser(AbstractUser):
    progres = models.IntegerField(default=1)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set', 
        blank=True,
        help_text='Specific permissions for this user.'
    )