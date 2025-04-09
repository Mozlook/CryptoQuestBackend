from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Zagadki, Bledy
from .serializers import BledySerializer, LoginSerializer, UserSerializer
from django.middleware.csrf import get_token
from django.contrib.auth import login
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
            return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({'message': 'Login successful', 'user_id': user.id, 'progres': user.progres})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProgressView(APIView):
    def post(self, request):
        user = request.user
        progres = request.data.get('progres')
        if progres is not None:
            user.progres = progres
            user.save()
            return Response({'message': 'Progress updated', 'progres': user.progres})
        return Response({'error': 'Progress value missing'}, status=status.HTTP_400_BAD_REQUEST)