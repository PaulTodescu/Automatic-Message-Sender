import csv
import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from person.models import Person

from .forms import CreateListForm
from .models import List


def check(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if re.search(regex, email):
        return 1
    return 0

@login_required
def create_list_view(request):
    form = CreateListForm(request.POST, request.FILES)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

        with open(obj.csv_file.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    if check(row[2]):
                        person, created = Person.objects.get_or_create(name=row[0], gender=row[1], email=row[2])
                        obj.people.add(person)
                    else:
                        person, created = Person.objects.get_or_create(name=row[0], gender=row[1], phone=row[2])
                        obj.people.add(person)
                    print(row[0])
                    line_count += 1

        return HttpResponseRedirect(reverse('view-list'))

    context = {
        'form': form
    }

    return render(request, "create_list.html", context)


@login_required
def view_lists(request):
    return render(request, "view_lists.html", {'lists': List.objects.all()})


@login_required
def delete_list(request, listid):
    List.objects.filter(id=listid).delete()
    return redirect(request.META['HTTP_REFERER'])
