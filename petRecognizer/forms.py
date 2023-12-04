from django import forms
from .models import PetImage

class PetImageForm(forms.ModelForm):
    class Meta:
        model = PetImage
        fields = ['image']