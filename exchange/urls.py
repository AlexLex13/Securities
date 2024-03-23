from . import views
from django.urls import path

exchange_patterns = [
    path('', views.exchange, name="exchange"),
    path('send/', views.send_preference, name="send_pref"),
]
