from django.shortcuts import render

from .forms import CreateListForm

# Create your views here.


def create_list_view(request):
    form = CreateListForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, "create_list.html", context)


