from rest_framework import serializers
from sentimentor.models import Sentimentor,Tickersentiment

class Sentimentorserializer(serializers.ModelSerializer):
    class Meta:
        model=Sentimentor
        fields="__all__"



class Tickerserializer(serializers.ModelSerializer):
    class Meta:
        model=Tickersentiment
        fields="__all__"