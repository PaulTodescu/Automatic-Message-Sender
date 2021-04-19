from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
import csv

from list.models import List


@login_required
def home(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


def send_msg(request):
    with open(List.objects.get(id=2).csv_file.path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # column
                line_count += 1
            else:
                print(row)
                line_count += 1

    return HttpResponseRedirect("/")
