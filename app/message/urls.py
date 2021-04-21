from django.urls import path
from .views import create_message, view_messages, choose_fields

urlpatterns = [
    path('create_message/', create_message, name="create-message"),
    path('choose_fields/', choose_fields, name="choose-fields"),
    path('view_messages/', view_messages, name="view-messages"),
]
