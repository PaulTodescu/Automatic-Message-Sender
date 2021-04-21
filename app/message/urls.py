from django.urls import path, re_path
from .views import create_message, view_messages, choose_fields, view_message

urlpatterns = [
    path('create_message/', create_message, name="create-message"),
    re_path(r'^choose_fields/(?P<messageid>\w+)/$', choose_fields, name="choose-fields"),
    re_path(r'^view_message/(?P<messageid>\w+)/$', view_message, name="view-message"),
    path('view_messages/', view_messages, name="view-messages"),
]
