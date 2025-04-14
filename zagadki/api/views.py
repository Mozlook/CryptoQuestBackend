from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Zagadki, Bledy
from .serializers import BledySerializer, RegistrationSerializer
from django.middleware.csrf import get_token
from django.contrib.auth import login, authenticate, get_user_model
from rest_framework.authtoken.models import Token
import json

class SprawdzProgres(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        progress = request.user.progress
        return Response({
            "progress": progress
        })

class SprawdzOdpowiedz(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    
    def post(self, request):
        user = request.user if request.user and request.user.is_authenticated else None
        odpowiedz = request.data.get('answer')

        if not odpowiedz:
            return Response({'error': 'Brak odpowiedzi'}, status=status.HTTP_400_BAD_REQUEST)

        numer_zagadki = user.progress if user else 1

        try:
            zagadka = Zagadki.objects.get(numer=numer_zagadki)
        except Zagadki.DoesNotExist:
            return Response({'error': 'Nie znaleziono zagadki'}, status=status.HTTP_404_NOT_FOUND)

        if odpowiedz.strip().lower() == zagadka.kod.strip().lower():
            if user:
                user.progress += 1
                user.save()
                return Response({'answer': True}, status=status.HTTP_200_OK)
            else:
                return Response({'answer':True,
                                 'progress': 2}, status=status.HTTP_200_OK)
        else:
            return Response({'answer': False}, status=status.HTTP_200_OK)
        
    
def get_csrf_token(request):
    csrf_token = get_token(request)
    response_data = {
        "detail": "CSRF token generated",
        "csrftoken": csrf_token 
    }
    response = JsonResponse(response_data)
    
    response.set_cookie(
        'csrftoken',
        csrf_token,
        max_age=3600,
        secure=True,
        httponly=False,
        samesite='None' 
    )
    
    return response

class BledyList(APIView):
    def post(self, request):
        serializer = BledySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            user = serializer.save()
            return Response(
                {
                    'message': 'User created successfully',
                    'email': user.email,
                    'username': user.username
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)