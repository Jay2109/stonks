from rest_framework import serializers
from .models import Predictions

class Predictionserializer(serializers.ModelSerializer):
    class Meta:
        model=Predictions
        fields="__all__"