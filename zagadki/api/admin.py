from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Zagadki, Bledy, CustomUser

admin.site.register(Zagadki)
admin.site.register(Bledy)
admin.site.register(CustomUser)