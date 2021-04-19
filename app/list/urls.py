from django.urls import path
from .views import create_list_view, view_lists

urlpatterns = [
    path('create_list/', create_list_view),
    path('view_lists/', view_lists, name="view-list"),

]
