from rest_framework import serializers
from .models import Zagadki, Bledy

class ZagadkiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zagadki
        fields = ['numer', 'tekst_zagadki', 'kod']

class BledySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bledy
        fields = ['id', 'numer', 'opis']
