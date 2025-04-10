from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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

class User(AbstractUser):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    progress = models.IntegerField(default=1)
    first_name = None
    last_name = None

    # class Meta:
    #     db_table = 'users' 
    #     verbose_name = _('User')
    #     verbose_name_plural = _('Users')