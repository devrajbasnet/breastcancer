from django import forms
from .models import BreastCancerData

class BreastDataForm(forms.ModelForm):
    class Meta:
        model = BreastCancerData
        fields = '__all__'
