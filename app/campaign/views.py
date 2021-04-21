from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Campaign

from .forms import CreateCampaignForm


@login_required
def create_campaign(request):
    form = CreateCampaignForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('view-campaigns'))

    context = {
        'form': form
    }

    return render(request, "create_campaign.html", context)


@login_required
def view_campaigns(request):
    return render(request, "view_campaigns.html", {"campaigns": Campaign.objects.all()})
