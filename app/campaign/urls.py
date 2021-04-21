from django.urls import path, re_path
from .views import view_campaigns, create_campaign

urlpatterns = [
    path('view_campaigns/', view_campaigns, name="view-campaigns"),
    path('create_campaign/', create_campaign, name="create-campaign"),
]
