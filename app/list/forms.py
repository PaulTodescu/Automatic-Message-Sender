from django import forms

from .models import List


class CreateListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = [
            'name',
            'date',
            'reason',
            'type'
        ]
