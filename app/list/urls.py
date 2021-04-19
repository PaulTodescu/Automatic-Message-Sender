from django.urls import path
from .views import create_list_view

urlpatterns = [
    path('create_list', create_list_view)
]

