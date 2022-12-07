from django import forms

from .models import ReviewRating,Architects

class ReviewForm(forms.ModelForm):
    class Meta:
        model=ReviewRating
        fields=['subject','review','rating']

class ArchitectsForm(forms.ModelForm):
    class Meta:
        model=Architects
        fields='__all__'


