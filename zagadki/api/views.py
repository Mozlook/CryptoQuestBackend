from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Zagadki, Bledy
from .serializers import BledySerializer
from django.middleware.csrf import get_token
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

class BledyList(APIView):
    def post(self, request):
        serializer = BledySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

def get_csrf_token(request):
    response = JsonResponse({"detail": "CSRF cookie set"})
    response["X-CSRFToken"] = get_token(request) 
    return response
