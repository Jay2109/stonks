from django.urls import path,include
from . import views

urlpatterns = [
    path('sentiment/', views.sentiment_data),
    path('sentiment/<slug:slug>/',views.sentiment_ticker),
]