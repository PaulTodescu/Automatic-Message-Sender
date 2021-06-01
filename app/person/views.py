from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Person

@login_required
def view_people(request):
    return render(request, "view_people.html", {'people': Person.objects.all()})
