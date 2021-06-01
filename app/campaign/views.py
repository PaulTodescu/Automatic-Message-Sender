import os
import csv
from email.mime.image import MIMEImage
import re

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Campaign

from django.core.mail import EmailMultiAlternatives
from app.settings import EMAIL_HOST_USER

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


def check(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if re.search(regex, email):
        return 1
    return 0


@login_required()
def send_msg(request, campaignid):
    try:
        campaign_obj = Campaign.objects.get(id=campaignid)
        # list_type = campaign_obj.list.type

        sms_ids = requests.get("https://app.smso.ro/api/v1/senders/?apiKey=" + API_KEY)

        if sms_ids.status_code == 200:
            sms_ids = sms_ids.json()[0]['id']
        else:
            raise Http404

        people_queryset = campaign_obj.list.people.all()

        for person in people_queryset:
            if person.email:
                images = re.findall(r'src="cid:(.*?)"', campaign_obj.message.message)
                email_content = EmailMultiAlternatives(
                    campaign_obj.title,
                    campaign_obj.message.message,
                    EMAIL_HOST_USER,
                    [person.email]
                )
                email_content.attach_alternative(campaign_obj.message.message, "text/html")
                email_content.mixed_subtype = 'related'

                media_path = 'media/uploads/images/'

                for f in images:
                    fp = open(os.path.join(media_path, f), 'rb')
                    img = MIMEImage(fp.read())
                    fp.close()
                    img.add_header('Content-ID', '<{}>'.format(f))
                    email_content.attach(img)

                email_content.send()
            # elif person.phone:
            #     url = 'https://app.smso.ro/api/v1/send/?apiKey=' + API_KEY
            #     payload = {'to':person.phone,
            #                 'sender': sms_ids,
            #                 'body': campaign_obj.message.message}
            #     requests.post(url, data=payload)


    # with open(campaign_obj.list.csv_file.path) as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     line_count = 0
    #
    #     images = re.findall(r'src="cid:(.*?)"', campaign_obj.message.message)
    #
    #     for row in csv_reader:
    #         if line_count == 0:
    #             print(f'Column names are {", ".join(row)}')
    #             line_count += 1
    #         else:
    #             if list_type == "Phone":
    #                 print(row[0])
    #                 url = 'https://app.smso.ro/api/v1/send/?apiKey=' + API_KEY
    #                 payload = {'to': row[0],
    #                            'sender': sms_ids,
    #                            'body': campaign_obj.message.message}
    #                 requests.post(url, data=payload)
    #
    #             elif list_type == "Email":
    #                 print(row[0])
    #
    #                 if check(row[0]):
    #
    #                     email_content = EmailMultiAlternatives(
    #                         campaign_obj.title,
    #                         campaign_obj.message.message,
    #                         EMAIL_HOST_USER,
    #                         [row[0]]
    #                     )
    #                     email_content.attach_alternative(campaign_obj.message.message, "text/html")
    #                     email_content.mixed_subtype = 'related'
    #
    #                     media_path = 'media/uploads/images/'
    #
    #                     for f in images:
    #                         fp = open(os.path.join(media_path, f), 'rb')
    #                         img = MIMEImage(fp.read())
    #                         fp.close()
    #                         img.add_header('Content-ID', '<{}>'.format(f))
    #                         email_content.attach(img)
    #
    #                     email_content.send()
    #
    #             else:
    #                 if check(row[0]) == 0:
    #                     url = 'https://app.smso.ro/api/v1/send/?apiKey=' + API_KEY
    #                     payload = {'to': row[0],
    #                                'sender': sms_ids,
    #                                'body': campaign_obj.message.message}
    #                     requests.post(url, data=payload)
    #
    #                 if check(row[0]) == 1:
    #                     send_mail(
    #                         campaign_obj.title,
    #                         campaign_obj.message.message,
    #                         settings.EMAIL_HOST_USER,
    #                         [row[0]]
    #                     )
    #
    #             line_count += 1

    except Exception as e:
        print(e)
        raise Http404

    return HttpResponseRedirect(reverse('view-campaigns'))
