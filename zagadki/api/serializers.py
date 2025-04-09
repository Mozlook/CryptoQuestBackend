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

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)
    user_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'progres', 'groups', 'user_permissions']

    def create(self, validated_data):
        password = validated_data.pop('password')  # Usuwamy hasło, by je zahaszować
        user = User.objects.create(**validated_data)  # Tworzymy użytkownika
        user.set_password(password)  # Haszujemy hasło
        user.save()  # Zapisujemy użytkownika do bazy danych
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        
        # Generowanie tokenów
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }