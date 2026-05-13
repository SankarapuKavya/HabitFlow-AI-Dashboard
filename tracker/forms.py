from django import forms
from .models import Habit


class HabitForm(forms.ModelForm):

    class Meta:

        model = Habit

        fields = [
            'title',
            'description',
            'category'
        ]

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter habit title'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

        }