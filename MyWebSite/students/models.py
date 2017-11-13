#!/usr/bin/python
#coding:utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Student(models.Model):
    firstName = models.CharField(max_length=200)
    
    lastName = models.CharField(max_length=200)

    phoneRegex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    phoneNumber = models.CharField(max_length=200, validators=[phoneRegex], blank=True)
    
    def __init__(self, *args, **kws):
        super(Student, self).__init__(*args, **kws)
        self.gradeList = []

    def __str__(self):
        return self.firstName + self.lastName + self.phoneNumber

    def addGrade(self, grade):
        self.gradeList.append(grade)

class Grade(models.Model):
    student = models.ForeignKey(Student, related_name='grade')

    subject1Score = models.IntegerField()
    
    subject2Score = models.IntegerField()
    
    subject3Score = models.IntegerField()
    
    examNumber = models.IntegerField() 

    def __str__(self):
        return '%d, %d, %d' % (
            self.subject1Score, self.subject2Score, self.subject3Score,)

    class Meta:
        ordering = ['examNumber']

class User(AbstractUser):
    """
    Custom user class.
    """

    phoneRegex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    phoneNumber = models.CharField(max_length=200, validators=[phoneRegex], blank=True)

    MondayClass = models.BooleanField(default=True)

RATING_CHOICES = ((1, u"非常沒有幫助"), (2, u"沒有幫助"), (3, u"不太有幫助"), (4, u"有幫助"), (5, u"很有幫助"), (6, u"非常有幫助"),)

class EvaluationScheme(models.Model):
    title = models.CharField(max_length=200)

class EvaluationQuestion(models.Model):
    question = models.CharField(max_length=200)
    evaluation = models.ForeignKey(EvaluationScheme)
    visualizationId = models.IntegerField(default=1)

    def __unicode__(self):
        return self.question

class EvaluationAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(EvaluationQuestion)
    answer = models.SmallIntegerField(choices=RATING_CHOICES)
        

