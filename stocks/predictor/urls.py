from django.urls import path,include
from .import views

urlpatterns = [
    path('prediction/<slug:slug>/', views.prediction_data),
]