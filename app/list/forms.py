from django import forms
from .models import List

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = '__all__'
        widgets = {
            'date': DateInput()
        }
