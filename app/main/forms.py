from django import forms


class LoginForm(forms.Form):
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'style': "width:100%;"}))
