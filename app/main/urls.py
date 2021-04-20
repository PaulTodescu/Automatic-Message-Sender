from django.contrib import admin
from django.urls import path
from .views import home, LoginPage, send_msg

urlpatterns = [
    path('', home),
    path('login/', LoginPage.as_view(), name='login'),
    path('send_msg/', send_msg)
]

