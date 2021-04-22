from django import forms
from .models import Message


class CreateMessageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    diff_gender = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': "form-check", 'required': "false"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Message")

    class Meta:
        model = Message
        fields = '__all__'

class ChooseFields(forms.Form):
    pass
