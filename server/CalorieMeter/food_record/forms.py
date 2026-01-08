from django import forms
from .models import FoodRecord

class FoodRecordForm(forms.ModelForm):
    class Meta:
        model = FoodRecord
        fields = ['image']
