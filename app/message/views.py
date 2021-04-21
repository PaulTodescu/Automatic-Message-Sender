import csv
import re

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Message

from .forms import CreateMessageForm, ChooseFields


@login_required
def create_message(request):
    form = CreateMessageForm(request.POST, request.FILES)
    print(request.POST)
    if form.is_valid():
        initial_obj = form.save(commit=False)
        initial_obj.save()
        path = initial_obj.csv_fields.path
        field_dict = {}
        to_fill_fields = re.findall(r'{xx[0-9]+}', initial_obj.message)
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            keys = next(csv_reader)
            values = next(csv_reader)
            for key, value in zip(keys, values):
                field_dict[key] = value

        CHOICES = []
        for key in keys:
            CHOICES.append((key, key))

        request.session['FILL_FIELDS'] = to_fill_fields
        request.session['CHOICES'] = CHOICES

        return HttpResponseRedirect(reverse('choose-fields'))

    context = {
        'form': form
    }

    return render(request, "create_message.html", context)


def choose_fields(request):
    new_fields = {}
    FILL_FIELDS = request.session.get("FILL_FIELDS")
    CHOICES = request.session.get("CHOICES")

    for field in FILL_FIELDS:
        new_fields[field] = forms.CharField(widget=forms.Select(choices=CHOICES))

    DynamicIngridientsForm = type('DynamicIngridientsForm',
                                  (ChooseFields,),
                                  new_fields)

    form = DynamicIngridientsForm(request.POST or None)

    print(request.POST)

    return render(request, "choose_fields.html", {'form': form})


@login_required
def view_messages(request):
    return render(request, "view_messages.html", {'messages': Message.objects.all()})
