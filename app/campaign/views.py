import os
import csv
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Campaign

from django.core.mail import send_mail
from django.conf import settings

from .forms import CreateCampaignForm

API_KEY = os.environ.get("SMSO_API_KEY")


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


@login_required
def delete_campaign(request, campaignid):
    Campaign.objects.filter(id=campaignid).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required()
def send_msg(request, campaignid):
    try:
        campaign_obj = Campaign.objects.get(id=campaignid)
        list_type = campaign_obj.list.type

        sms_ids = requests.get("https://app.smso.ro/api/v1/senders/?apiKey=" + API_KEY)

        if sms_ids.status_code == 200:
            sms_ids = sms_ids.json()[0]['id']
        else:
            raise Http404

        with open(campaign_obj.list.csv_file.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    if list_type == "Phone":
                        print(row[0])
                        url = 'https://app.smso.ro/api/v1/send/?apiKey=' + API_KEY
                        payload = {'to': row[0],
                                   'sender': sms_ids,
                                   'body': campaign_obj.message.message}
                        requests.post(url, data=payload)

                    elif list_type == "Email":
                        print(row[0])

                        # send email

                        send_mail(
                            campaign_obj.title,
                            campaign_obj.message.message,
                            settings.EMAIL_HOST_USER,
                            [row[0]]
                        )

                    line_count += 1
    except:
        raise Http404

    return HttpResponseRedirect(reverse('view-campaigns'))


