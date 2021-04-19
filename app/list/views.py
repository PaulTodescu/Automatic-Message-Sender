from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateListForm
from .models import List

def create_list_view(request):
    form = CreateListForm(request.POST or None)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('view-list'))

    context = {
        'form': form
    }

    return render(request, "create_list.html", context)

def view_lists(request):
    return render(request, "view_lists.html", {'lists': List.objects.all()})


