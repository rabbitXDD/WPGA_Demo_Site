from django import forms
from django.db import models

from students.models import User, EvaluationAnswer, EvaluationQuestion, EvaluationScheme, RATING_CHOICES

class ValuationsForm(forms.ModelForm):
    class Meta:
        model = EvaluationAnswer
        fields = ['answer', ]

        widgets = {
            'answer': forms.RadioSelect(choices=RATING_CHOICES),
        }
    