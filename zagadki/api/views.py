from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators import api_view
from django.http import JsonResponse
from .models import Zagadki, Bledy
from .serializers import BledySerializer, RegistrationSerializer
from django.middleware.csrf import get_token
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import json


def sprawdz_zagadke(request):
    if request.method == 'POST':  # Tylko POST
        try:
            # Parsowanie danych JSON
            data = json.loads(request.body)
            numer_zagadki = data.get('numer')
            odpowiedz = data.get('tekst')

            # Znalezienie zagadki na podstawie numeru
            zagadka = Zagadki.objects.get(numer=numer_zagadki)
            
            # Sprawdzanie, czy odpowiedź jest poprawna
            if odpowiedz == zagadka.kod:
                return JsonResponse({'result': True})
            else:
                return JsonResponse({'result': False})
        except Zagadki.DoesNotExist:
            return JsonResponse({'error': 'Zagadki o takim numerze nie znaleziono'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    else:
        # Obsługuje tylko POST, inne metody zwracają błąd
        return JsonResponse({'error': 'Metoda dozwolona to POST'}, status=405)

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
            