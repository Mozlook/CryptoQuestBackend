from rest_framework import serializers
from .models import Zagadki, Bledy, CustomUser
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.tokens import RefreshToken

class ZagadkiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zagadki
        fields = ['numer', 'tekst_zagadki', 'kod']

class BledySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bledy
        fields = ['id', 'numer', 'opis']

User = get_user_model()
