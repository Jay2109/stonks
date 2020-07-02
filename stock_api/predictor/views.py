from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Predictions
from .serializers import Predictionserializer

# Create your views here.
@csrf_exempt

def prediction_data(request,slug):
    try:
        prediction_data=Predictions.objects.filter(sym_name=slug).last()
    except Predictions.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method=="GET":
        serializer = Predictionserializer(prediction_data)
        return JsonResponse(serializer.data)
