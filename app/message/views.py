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

        id = str(initial_obj.id)
        request.session['FILL_FIELDS' + id] = to_fill_fields
        request.session['CHOICES' + id] = CHOICES
        request.session['FIELD_DICT' + id] = field_dict

        return HttpResponseRedirect(reverse('choose-fields', kwargs={'messageid': initial_obj.id}))

    context = {
        'form': form
    }

    return render(request, "create_message.html", context)


@login_required
def choose_fields(request, messageid):
    if messageid:
        new_fields = {}
        FILL_FIELDS = request.session.get("FILL_FIELDS" + messageid)
        CHOICES = request.session.get("CHOICES" + messageid)
        FIELD_DICT = request.session.get("FIELD_DICT" + messageid)

        for field in FILL_FIELDS:
            new_fields[field] = forms.CharField(widget=forms.Select(choices=CHOICES))

        DynamicFieldForm = type('DynamicIngridientsForm',
                                (ChooseFields,),
                                new_fields)
        form = DynamicFieldForm(request.POST or None)

        if form.is_valid():
            try:
                message_obj = Message.objects.get(id=messageid)
                new_msg = message_obj.message
                for field in FILL_FIELDS:
                    new_msg = new_msg.replace(field, FIELD_DICT[form.cleaned_data[field]])
                message_obj.message = new_msg
                message_obj.save()
                request.session.modified = True
                del request.session["FILL_FIELDS" + messageid]
                del request.session["CHOICES" + messageid]
                del request.session["FIELD_DICT" + messageid]

            except Message.DoesNotExist:
                return render(request, "choose_fields.html", {'form': form})

        return render(request, "choose_fields.html", {'form': form})


@login_required
def view_messages(request):
    return render(request, "view_messages.html", {'messages': Message.objects.all()})
