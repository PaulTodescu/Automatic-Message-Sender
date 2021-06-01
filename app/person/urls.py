from django.urls import path
from .views import view_people

urlpatterns = [
    path('view_people/', view_people, name="view-people"),
]
