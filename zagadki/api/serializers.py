from rest_framework import serializers
from .models import Zagadki

class ZagadkiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zagadki
        fields = ['numer', 'tekst_zagadki', 'kod']
