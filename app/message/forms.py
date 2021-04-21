from django import forms
from .models import Message


class CreateMessageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    diff_gender = forms.CharField(widget=forms.CheckboxInput(attrs={'class': "form-check"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Message")

    class Meta:
        model = Message
        fields = '__all__'

class ChooseFields(forms.Form):
    pass
