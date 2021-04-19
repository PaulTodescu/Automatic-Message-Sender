from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")
