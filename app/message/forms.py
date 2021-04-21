from django import forms
from .models import Message


class CreateMessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Message")

    class Meta:
        model = Message
        fields = '__all__'

class ChooseFields(forms.Form):
    pass
