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

from image.models import Image

from django.core.mail import send_mail
from django.conf import settings

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

            # get the images used in the message

            # image_paths = re.findall(r'src="cid:(.*?)"', campaign_obj.message.message)
            # images = []
            # for el in image_paths:
            #     images.append(el.split('/')[-1])

            images = re.findall(r'src="cid:(.*?)"', campaign_obj.message.message)

            # images = []
            # image_paths = list(Image.objects.all().values_list('image_file', flat=True))
            # for path in image_paths:
            #     images.append(path.split('/')[-1])

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

                        # send_mail(
                        #     campaign_obj.title,
                        #     campaign_obj.message.message,
                        #     settings.EMAIL_HOST_USER,
                        #     [row[0]]
                        # )

                        email_content = EmailMultiAlternatives(
                            campaign_obj.title,
                            campaign_obj.message.message,
                            EMAIL_HOST_USER,
                            [row[0]])
                        email_content.attach_alternative(campaign_obj.message.message, "text/html")
                        email_content.mixed_subtype = 'related'

                        media_path = 'media/uploads/images/'

                        for f in images:
                            fp = open(os.path.join(media_path, f), 'rb')
                            img = MIMEImage(fp.read())
                            fp.close()
                            img.add_header('Content-ID', '<{}>'.format(f))
                            email_content.attach(img)

                        # image_path = os.path.join(media_path, 'new_image.png')
                        # fp = open(image_path, 'rb')
                        # img = MIMEImage(fp.read())
                        # fp.close()
                        # img.add_header('Content-ID', '<{}>'.format('new_image.png'))
                        # email_content.attach(img)

                        email_content.send()

                    line_count += 1
    except:
        raise Http404

    return HttpResponseRedirect(reverse('view-campaigns'))
