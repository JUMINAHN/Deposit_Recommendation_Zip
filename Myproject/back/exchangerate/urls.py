from django.urls import path
from . import views

urlpatterns = [
    path('exchange-rates/', views.exchange_rates, name='exchange_rates'),
]
