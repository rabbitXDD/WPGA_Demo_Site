from django import forms
from django.db import models

from students.models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['firstName', 'lastName', 'phoneNumber']

        widgets = {
            'firstName': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'David'                
                }
            ),
            'lastName': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Lee'                
                }
            ),
            'phoneNumber': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '+886999999999'
                }
            ),
        }
        labels = {
            'firstName':'first name:',
            'lastName':'last name:',
            'phoneNumber':'phone number:',
        }

    