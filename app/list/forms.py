from django import forms
from .models import List


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateListForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Name")
    date = forms.DateField(label="Date")
    reason = forms.CharField(max_length=20, label="Reason")
    type = forms.CharField(max_length=100, label="Type")
    csv_file = forms.FileField(label="CSV File")

    class Meta:
        model = List
        fields = '__all__'
        widgets = {
            'date': DateInput()
        }
