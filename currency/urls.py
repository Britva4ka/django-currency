from django.urls import path
from .views import currency


urlpatterns = [
    path('currency/', currency, name='currency')
]
