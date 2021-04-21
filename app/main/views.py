from xml.dom import minidom

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import csv
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

from list.models import List
from .forms import LoginForm
from django.contrib import messages
import base64


# def encrypt_alg1(text):
#     encoded_data = base64.b64encode(text)
#     return encoded_data


def decrypt_alg1(text):
    decoded_data = base64.b64decode(text)
    return decoded_data


@login_required
def home(request):
    return render(request, "index.html")


class LoginPage(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        loginForm = LoginForm()

        context = {
            'form': loginForm
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        loginForm = LoginForm(request.POST)  # create login form

        text = None

        if loginForm.is_valid():
            text = loginForm.cleaned_data['password']  # get the password from the form

        user = None

        confirmation = None

        xmldoc = minidom.parse('main/password.xml')  # get the password form xml

        value = "".join(
            el.nodeValue for el in xmldoc.getElementsByTagName('value')[0].childNodes if el.nodeType == el.TEXT_NODE)

        alg = "".join(
            el.nodeValue for el in xmldoc.getElementsByTagName('algorithm')[0].childNodes if
            el.nodeType == el.TEXT_NODE)

        password = None

        # check which encryption algorithm is used
        if alg == "a1":
            password = decrypt_alg1(value).decode()  # decrypt the password from xml

        # login user
        if text == password:
            user = authenticate(request, username='myuser', password=text)
            confirmation = "logged in"
        else:
            confirmation = "incorrect password"

        if user is not None:
            login(request, user)

        context = {
            'form': loginForm,
            'confirmation': confirmation
        }

        if confirmation == "logged in":
            return redirect("/")

        return render(request, self.template_name, context)


def logout_view(request):
    logout(request)
    return redirect('login')


def send_msg(request):
    with open(List.objects.get(id=2).csv_file.path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        field_obj = {}
        for field, field1 in zip(csv_reader[0], csv_reader[1]):
            field_obj[field] = field1

        print(field_obj)
        # for row in csv_reader:
        #     # column
        #     if line_count == 0:
        #
        #         line_count += 1
        #     else:
        #         print(row)
        #         line_count += 1

    return HttpResponseRedirect("/")
