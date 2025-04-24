from rest_framework import serializers
from .models import Zagadki, Bledy
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()

class ZagadkiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zagadki
        fields = ['numer', 'tekst_zagadki', 'kod']

class BledySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bledy
        fields = ['id', 'numer', 'opis','image']
        
class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True) 
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only': True},
            'email': {'required': True}
        }
        
    def validate(self, data):
        
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Hasła muszą być identyczne!'})
        return data
        
    def create(self, validated_data):
        validated_data.pop('password2', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


