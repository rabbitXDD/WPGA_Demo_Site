from django import forms
from django.db import models

from students.models import User

class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new user.
    """

    firstName = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'David'
            }
        ), 
        label="first name", 
        max_length=200
    )
    lastName = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Lee'
            }
        ), 
        label="last name", 
        max_length=200
    )

    phoneNumber = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '+886999999999'
            }
        ), 
        label="phone number", 
        max_length=200
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nuwa@gmail.com'
            }
        ), 
        label="email", 
        max_length=200
    )

    userName = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ), 
        label="user name", 
        max_length=200
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ), 
        label="password", 
        max_length=200
    )

    passwordConfirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ), 
        label="confirm password", 
        max_length=200
    )

    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'phoneNumber', 'userName', 
                  'password', 'passwordConfirm']

    def clean(self):
        """
        Verifies that the values entered into the password fields match
        """
        cleanedData = super(RegistrationForm, self).clean()
        password = cleanedData.get('password')
        passwordConfirm = cleanedData.get('passwordConfirm')

        if password != passwordConfirm:
            raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
                
        return cleanedData

    def clean_userName(self):
        userName = self.cleaned_data['userName']
        if User.objects.filter(username=userName):
            raise forms.ValidationError("User name has already exist, please type another one.")

        return userName