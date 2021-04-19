from django.contrib import admin
from django.urls import path
from .views import home, login, send_msg

urlpatterns = [
    path('', home),
    path('login/', login),
    path('send_msg/', send_msg)
]
