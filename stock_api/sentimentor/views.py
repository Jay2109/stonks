from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Sentimentor,Tickersentiment
from .serializers import Sentimentorserializer,Tickerserializer

# Create your views here.
@csrf_exempt

def sentiment_data(request):
    try:
        sentimentor_data=Sentimentor.objects.last()
    except Sentimentor.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method=="GET":
        serializer =Sentimentorserializer(sentimentor_data)
        return JsonResponse(serializer.data)

@csrf_exempt

def sentiment_ticker(request,slug):
    try:
        ticker_data=Tickersentiment.objects.filter(sym_name=slug).last()
    except Tickersentiment.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method=="GET":
        serializer = Tickerserializer(ticker_data)
        return JsonResponse(serializer.data)




