from django.urls import path, re_path
from .views import view_people, create_person, update_person

urlpatterns = [
    path('view_people/', view_people, name="view-people"),
    path('create_person/', create_person, name="create-person"),
    re_path(r'^update_person/(?P<person_id>\w+)/$', update_person, name="update-person"),
]
